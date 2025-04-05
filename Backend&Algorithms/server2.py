from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import joblib
import torch
from transformers import BertTokenizer, BertModel
import pandas as pd
from io import BytesIO
import xlsxwriter  # Para generar el Excel
import re
import logging
import ollama  # Se asume que esta librería está disponible para comunicarte con el LLM

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# Funciones de carga y procesamiento
# ---------------------------
def cargar_modelo(svm_file: str, pca_file: str, le_file: str):
    modelo_svm = joblib.load(svm_file)
    pca = joblib.load(pca_file)
    le = joblib.load(le_file)
    return modelo_svm, pca, le

# Inicializar BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model_bert = BertModel.from_pretrained('bert-base-uncased')

def procesar_con_bert(texto: str):
    inputs = tokenizer(texto, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model_bert(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

def clasificar_concepto(concepto: str, modelo_svm, pca, le):
    embedding = procesar_con_bert(concepto)
    embedding_pca = pca.transform([embedding])
    prediccion = modelo_svm.predict(embedding_pca)
    categoria = le.inverse_transform(prediccion)
    return categoria[0]

# ---------------------------
# Configuración de la aplicación FastAPI
# ---------------------------
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelos (asegúrate de tener los archivos correctos)
modelo_svm_cargado, pca_cargado, le_cargado = cargar_modelo(
    "modelo_svm_entrenado.pkl", "pca_entrenado.pkl", "le_entrenado.pkl"
)

# Prompt global para orientar al LLM
PROMPT_GLOBAL = (
    "Eres un asistente de finanzas personales. Responde preguntas y organiza ingresos y gastos del usuario. "
    "Cuando el usuario indique 'descargalo', se debe finalizar la conversación y generar el archivo Excel."
)

# Almacén global para el historial de conversación
global_chat_history = [{"role": "system", "content": PROMPT_GLOBAL}]

# Modelos de solicitud
class ConversationRequest(BaseModel):
    chat_history: list  # Lista de mensajes (cada mensaje es un diccionario con 'role' y 'content')

class FinalizeRequest(BaseModel):
    chat_history: list

# ---------------------------
# Endpoint para manejar la conversación
# ---------------------------
@app.post("/conversation")
def conversation(request: ConversationRequest):
    global global_chat_history
    try:
        # Agregar mensajes recibidos al historial global
        for msg in request.chat_history:
            global_chat_history.append(msg)
        
        # Llamada al LLM para obtener la respuesta (se usa ollama.chat)
        response_llm = ollama.chat(
            model="llama3.2:3b", 
            messages=global_chat_history
        )
        # Limpiar respuesta removiendo posibles secciones de <think>
        response_text = re.sub(r'<think>.*?</think>', '', response_llm["message"]["content"], flags=re.DOTALL).strip()
        global_chat_history.append({"role": "assistant", "content": response_text})
        return {"response": response_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in conversation: {str(e)}")

# ---------------------------
# Endpoint para finalizar la conversación y generar el Excel
# ---------------------------
@app.post("/finalize")
def finalize_conversation(request: FinalizeRequest):
    global global_chat_history
    try:
        # Agregar mensajes adicionales del request al historial global
        for msg in request.chat_history:
            global_chat_history.append(msg)
        
        # Instrucción para que el LLM extraiga y organice los datos estructurados
        extraction_instruction = (
            "Extrae y organiza los datos en formato: "
            "Concepto: <concepto>, Monto: <monto>, Categoria: <categoria>"
        )
        messages_for_extraction = global_chat_history + [{"role": "system", "content": extraction_instruction}]
        
        extraction_response = ollama.chat(
            model="llama3.2:3b",
            messages=messages_for_extraction
        )
        llm_output = extraction_response["message"]["content"]
        logger.info(f"LLM output for extraction:\n{llm_output}")
        
        # Parsear la salida estructurada
        registros = []
        for line in llm_output.strip().split("\n"):
            match = re.search(r"Concepto:\s*(.*?),\s*Monto:\s*([\d\.]+),\s*Categoria:\s*(.*)", line, re.IGNORECASE)
            if match:
                concepto = match.group(1).strip()
                try:
                    monto = float(match.group(2))
                except Exception:
                    monto = 0
                categoria = match.group(3).strip()
                registros.append({"concepto": concepto, "monto": monto, "categoria": categoria})
        
        # Si no se extrajeron registros, procesar mensajes de usuario individualmente
        if not registros:
            for msg in global_chat_history:
                if msg.get("role", "").lower() == "user":
                    texto = msg.get("content", "")
                    m = re.search(r"(\d+(?:\.\d+)?)", texto)
                    if m:
                        monto = float(m.group(1))
                        concepto = re.sub(r'\d+(?:\.\d+)?', '', texto).strip()
                        categoria = clasificar_concepto(concepto, modelo_svm_cargado, pca_cargado, le_cargado)
                        registros.append({"concepto": concepto, "monto": monto, "categoria": categoria})
        
        if not registros:
            raise HTTPException(status_code=400, detail="No se extrajeron datos para generar el Excel.")
        
        # Generar el archivo Excel con los datos extraídos
        df = pd.DataFrame(registros)
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
        raise HTTPException(status_code=500, detail=f"Error al finalizar la conversación: {str(e)}")
