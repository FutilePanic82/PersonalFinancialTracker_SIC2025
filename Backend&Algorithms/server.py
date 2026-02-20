"""
server.py — Personal Financial Tracker · FastAPI backend
==========================================================
Endpoints
---------
POST /conversation        — Chat with the LLM; extracts & classifies transactions
GET  /historial           — Return all stored transactions
POST /finalize            — Generate, save, and download Excel file
GET  /reportes            — List generated Excel reports
GET  /reportes/{id}/download — Download a specific report
POST /predict             — Polynomial-regression spending prediction
POST /metas               — LLM advice on budget goals
DELETE /reset             — Clear in-memory conversation (keeps DB records)
"""
from __future__ import annotations

import json
import logging
import re
import os
from datetime import datetime
from io import BytesIO


import pandas as pd
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from classifier import clasificar
from database import init_db, insertar_transaccion, obtener_transacciones, insertar_reporte, obtener_reportes
from llm_provider import llm_chat, LLM_MODE, LLM_MODEL
from predictor import predecir

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# ── DB bootstrap ───────────────────────────────────────────────────────────────
init_db()

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(title="Personal Financial Tracker API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── System prompt ──────────────────────────────────────────────────────────────
_SYSTEM_PROMPT = """Eres un asistente de finanzas personales amigable y conciso. 
Tu tarea principal es ayudar al usuario a registrar sus ingresos y gastos.
Cuando el usuario mencione una transacción (gasto o ingreso), extrae la información
y confirma que fue registrada. 
Responde siempre en español y de forma breve (máximo 3 oraciones).
Si el usuario dice 'finalizar', 'descárgalo' o 'generar excel', confirma que puede
pulsar el botón de descarga."""

# ── In-memory conversation (single user) ───────────────────────────────────────
_chat_history: list[dict] = [{"role": "system", "content": _SYSTEM_PROMPT}]

# ── Extraction prompt injected silently ────────────────────────────────────────
_EXTRACTION_SYSTEM = """Eres un extractor de datos financieros.
A partir del mensaje del usuario extrae TODAS las transacciones mencionadas.
Devuelve SOLO un array JSON (sin markdown) con objetos:
{"concepto": string, "monto": number, "tipo": "gasto"|"ingreso"}
Si no hay transacciones, devuelve [].
Ejemplo: [{"concepto":"comida","monto":200,"tipo":"gasto"}]"""


# ── Pydantic models ────────────────────────────────────────────────────────────
class ConversationRequest(BaseModel):
    chat_history: list[dict]


class PredictRequest(BaseModel):
    ingresos: float
    hijos: int
    edad: int
    educacion: int          # 0=Primaria 1=Secundaria 2=Universidad 3=Posgrado


class MetasRequest(BaseModel):
    metas: list[dict]       # [{nombre: str, valor: int}]


# ── Helpers ────────────────────────────────────────────────────────────────────
def _llm(messages: list[dict]) -> str:
    """Call the configured LLM backend (Ollama / OpenAI / Groq)."""
    return llm_chat(messages)


def _extract_transactions(user_msg: str) -> list[dict]:
    """
    Ask the LLM to extract structured transactions from user_msg.
    Returns a list of dicts: {concepto, monto, tipo}.
    """
    messages = [
        {"role": "system", "content": _EXTRACTION_SYSTEM},
        {"role": "user",   "content": user_msg},
    ]
    raw = _llm(messages)
    logger.info("Extraction raw output: %s", raw)
    # Try JSON parse; fall back to regex if LLM wraps in markdown
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        data = json.loads(clean)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    # Fallback: simple regex
    results = []
    for m in re.finditer(
        r'"concepto"\s*:\s*"([^"]+)".*?"monto"\s*:\s*([\d.]+).*?"tipo"\s*:\s*"([^"]+)"',
        clean,
        re.DOTALL,
    ):
        results.append({
            "concepto": m.group(1),
            "monto": float(m.group(2)),
            "tipo": m.group(3),
        })
    return results


# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.post("/conversation")
def conversation(request: ConversationRequest):
    global _chat_history
    try:
        # Append new messages from the frontend to the server-side history.
        for msg in request.chat_history:
            if msg.get("role") in ("user", "assistant") and msg not in _chat_history:
                _chat_history.append(msg)

        # Last user message for silent extraction
        last_user = next(
            (m["content"] for m in reversed(request.chat_history) if m["role"] == "user"),
            "",
        )

        # 1. Extract transactions (silent call)
        transactions = _extract_transactions(last_user)
        saved = []
        for tx in transactions:
            concepto = str(tx.get("concepto", "")).strip()
            try:
                monto = float(tx.get("monto", 0))
            except (ValueError, TypeError):
                continue
            tipo_raw = str(tx.get("tipo", "gasto")).lower()
            tipo = "ingreso" if "ingreso" in tipo_raw else "gasto"
            if monto <= 0 or not concepto:
                continue
            categoria = clasificar(concepto)
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            insertar_transaccion(fecha, concepto, monto, categoria, tipo)
            saved.append({
                "concepto": concepto,
                "monto": monto,
                "categoria": categoria,
                "tipo": tipo,
            })
            logger.info("Saved transaction: %s", saved[-1])

        # 2. LLM conversational reply
        response_text = _llm(_chat_history)
        _chat_history.append({"role": "assistant", "content": response_text})

        return {"response": response_text, "transacciones_detectadas": saved}

    except Exception as exc:
        logger.exception("Error in /conversation")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/historial")
def historial():
    try:
        rows = obtener_transacciones()
        return {"transacciones": rows}
    except Exception as exc:
        logger.exception("Error in /historial")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/finalize")
def finalize():
    try:
        rows = obtener_transacciones()
        if not rows:
            raise HTTPException(
                status_code=400, detail="No hay transacciones guardadas para exportar."
            )

        df     = pd.DataFrame(rows)
        
        # 1. Generate filename with timestamp
        now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Reporte_Financiero_{now_str}.xlsx"
        
        # 2. Ensure directory
        base_dir = os.path.dirname(__file__)
        reports_dir = os.path.join(base_dir, "reportes")
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, filename)

        # 3. Write to disk
        with pd.ExcelWriter(filepath, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Finanzas")
            # Light formatting
            wb  = writer.book
            ws  = writer.sheets["Finanzas"]
            hdr = wb.add_format({"bold": True, "bg_color": "#1e1b4b", "font_color": "#ffffff"})
            for col_num, col_name in enumerate(df.columns):
                ws.write(0, col_num, col_name, hdr)
                ws.set_column(col_num, col_num, max(len(col_name) + 4, 16))

        # 4. Save to DB
        insertar_reporte(datetime.now().strftime("%Y-%m-%d %H:%M"), filename, filepath)

        # 5. Return file
        return FileResponse(
            path=filepath, 
            filename=filename, 
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error in /finalize")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/reportes")
def listar_reportes():
    """List all generated reports for history."""
    try:
        return obtener_reportes()
    except Exception as exc:
        logger.exception("Error in /reportes")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/reportes/{report_id}/download")
def descargar_reporte(report_id: int):
    """Download an old report."""
    try:
        reports = obtener_reportes()
        report = next((r for r in reports if r["id"] == report_id), None)
        if not report:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        filepath = report["path"]
        if not os.path.exists(filepath):
             raise HTTPException(status_code=404, detail="Archivo físico no encontrado")

        return FileResponse(
            path=filepath,
            filename=report["nombre"],
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error in /reportes/download")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/predict")
def predict(request: PredictRequest):
    try:
        result = predecir(
            ingresos=request.ingresos,
            hijos=request.hijos,
            edad=request.edad,
            educacion=request.educacion,
        )
        return result
    except Exception as exc:
        logger.exception("Error in /predict")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/metas")
def metas_advice(request: MetasRequest):
    try:
        metas_str = "\n".join(
            f"- {m['nombre']}: {m['valor']}%" for m in request.metas
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un asesor financiero experto. "
                    "El usuario te comparte su presupuesto deseado por categoría (en %). "
                    "Da consejos breves y concretos sobre si la distribución es saludable, "
                    "qué ajustaria y por qué. Responde en español, máximo 5 puntos breves."
                ),
            },
            {
                "role": "user",
                "content": f"Mi distribución de presupuesto:\n{metas_str}",
            },
        ]
        advice = _llm(messages)
        return {"response": advice}
    except Exception as exc:
        logger.exception("Error in /metas")
        raise HTTPException(status_code=500, detail=str(exc))


@app.delete("/reset")
def reset_conversation():
    global _chat_history
    _chat_history = [{"role": "system", "content": _SYSTEM_PROMPT}]
    return {"message": "Conversación reiniciada correctamente."}
