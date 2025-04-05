from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import pandas as pd
from io import BytesIO
import json
import logging
import ollama
from fastapi.middleware.cors import CORSMiddleware

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prompt global
PROMPT_GLOBAL = (
    "Eres un asistente de finanzas personales. Responde preguntas y organiza ingresos y gastos del usuario. "
    "Cuando el usuario indique 'descargalo', se debe finalizar la conversación y generar el archivo Excel. "
    "Extrae y organiza los datos en formato JSON con los campos: concepto, monto, categoria."
)

global_chat_history = [{"role": "system", "content": PROMPT_GLOBAL}]

# Modelos de solicitud
class ConversationRequest(BaseModel):
    chat_history: list

class FinalizeRequest(BaseModel):
    chat_history: list

@app.post("/conversation")
def conversation(request: ConversationRequest):
    global global_chat_history
    try:
        global_chat_history.extend(request.chat_history)

        response_llm = ollama.chat(
            model="llama3.2:3b",  # Se eliminó el espacio extra
            messages=global_chat_history
        )

        # Validar respuesta del LLM
        if "message" not in response_llm or "content" not in response_llm["message"]:
            raise HTTPException(status_code=500, detail="El LLM no devolvió una respuesta válida.")

        response_text = response_llm["message"]["content"].strip()

        global_chat_history.append({"role": "assistant", "content": response_text})
        return {"response": response_text}

    except Exception as e:
        logger.error(f"Error en la conversación: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en conversación: {str(e)}")

@app.post("/finalize")
def finalize_conversation(request: FinalizeRequest):
    global global_chat_history
    try:
        global_chat_history.extend(request.chat_history)

        messages_for_extraction = global_chat_history + [
            {"role": "system", "content": "Responde solo con JSON sin texto adicional. "
                "El formato esperado es: {\"datos\": [{\"concepto\": \"Nombre\", \"monto\": 0, \"categoria\": \"ingreso/gasto\"}]}"}
        ]

        extraction_response = ollama.chat(
            model="llama3.2:3b",  # Se eliminó el espacio extra
            messages=messages_for_extraction
        )

        # Validar respuesta del LLM
        if "message" not in extraction_response or "content" not in extraction_response["message"]:
            raise HTTPException(status_code=500, detail="El LLM no devolvió una respuesta válida.")

        llm_output = extraction_response["message"]["content"].strip()
        logger.info(f"LLM Output: {llm_output}")

        try:
            extracted_data = json.loads(llm_output)
            if "datos" not in extracted_data or not isinstance(extracted_data["datos"], list):
                raise ValueError("El JSON generado no tiene el formato esperado.")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="El LLM devolvió una respuesta no válida en JSON.")

        df = pd.DataFrame(extracted_data["datos"])
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Gastos e Ingresos")
        output.seek(0)

        return Response(
            output.read(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=gastos_ingresos.xlsx"}
        )

    except Exception as e:
        logger.error(f"Error al finalizar la conversación: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al finalizar la conversación: {str(e)}")
