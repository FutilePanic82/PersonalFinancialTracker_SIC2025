from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
from fastapi.middleware.cors import CORSMiddleware
import re
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
from sklearn.svm import SVC
import joblib
import json

app = FastAPI()

# Permitir CORS para Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Ajusta si Angular está en otro dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo y tokenizador de BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")

# Cargar el modelo SVM entrenado, el scaler y el label encoder
try:
    svm_model = joblib.load("svm_modelo.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    print("✅ Modelo SVM, scaler y label_encoder cargados correctamente.")
except FileNotFoundError as e:
    raise RuntimeError(f"❌ Error al cargar los modelos: {e}")

# Categorías predefinidas para el SVM
categorias = [
    "Alimentación", "Vivienda", "Transporte", "Salud", "Educación", 
    "Entretenimiento y ocio", "Ropa y accesorios", "Tecnología y gadgets", 
    "Viajes y vacaciones", "Ahorro personal", "Inversiones", "Donaciones y caridad"
]

# Historial de conversación
chat_history = []

# Prompt global (se usa solo al inicio)
global_prompt = {
    "role": "system",
    "content": "Eres un agente especializado en finanzas personales. Responde solo en español. Tu objetivo es generar un archivo Excel con los gastos mensuales del usuario. Debes hacer preguntas hasta obtener toda la información necesaria y hacerlas una a una..."
}

# Modelo de datos para la solicitud
class PromptRequest(BaseModel):
    prompt: str

# Función para procesar con BERT
def procesar_con_bert(texto: str):
    """
    Convierte el texto en un vector numérico utilizando BERT.
    """
    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # Devuelve el vector de características (embeddings) de la capa CLS
    return outputs.last_hidden_state[:, 0, :].numpy().flatten()

# Función para clasificar el concepto con SVM
def clasificar_concepto(concepto: str):
    """
    Obtiene el embedding de BERT, lo normaliza con el scaler
    y clasifica usando el modelo SVM.
    """
    embedding = procesar_con_bert(concepto)  # Convertir texto a embedding con BERT
    
    # Normalizar el embedding con el scaler entrenado
    embedding = scaler.transform([embedding])  # ← Agregando esta línea

    # Clasificar con el modelo SVM
    categoria_pred = svm_model.predict(embedding)

    # Convertir el índice numérico a su categoría original
    categoria = label_encoder.inverse_transform(categoria_pred)[0]
    
    return categoria

# Función para extraer monto y clasificar si es ingreso o egreso
def extraer_monto_y_tipo(texto: str):
    """
    Extrae el monto y clasifica si es ingreso o egreso.
    """
    # Aquí puedes usar una expresión regular para extraer montos y decidir si es ingreso o egreso
    monto = None
    tipo = "egreso"  # Por defecto asumimos egreso

    # Buscando un patrón de monto (en este caso en pesos)
    match = re.search(r"(\d+(?:[\.,]\d+)?)\s*(pesos|€|USD)?", texto)
    if match:
        monto = match.group(1)
        # Si el monto está asociado a ingresos, se clasifica como ingreso
        if "ingreso" in texto or "recibido" in texto:
            tipo = "ingreso"
    
    return monto, tipo

@app.post("/generate")
def generate_response(request: PromptRequest):
    global chat_history

    try:
        # Solo agregamos el prompt global en la primera interacción
        if not chat_history:
            chat_history.append(global_prompt)

        # Agregar la entrada del usuario al historial
        chat_history.append({"role": "user", "content": request.prompt})

        # Llamar a Ollama con el historial de la conversación
        response = ollama.chat(
            model="llama3.2:3b",
            messages=chat_history
        )

        # Extraer la respuesta del modelo
        raw_response = response["message"]["content"]

        # Limpiar respuesta eliminando cualquier bloque <think>
        cleaned_response = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()

        # Agregar la respuesta al historial para mantener el contexto
        chat_history.append({"role": "assistant", "content": cleaned_response})

        # Extraer monto y tipo (ingreso/egreso)
        monto, tipo = extraer_monto_y_tipo(cleaned_response)

        # Clasificar el concepto con BERT y SVM
        categoria = clasificar_concepto(cleaned_response)

        # Generar un JSON con la respuesta
        json_response = {
            "concepto": cleaned_response,
            "categoria": categoria,
            "monto": monto,
            "tipo": tipo
        }

        return {"response": cleaned_response, "clasificado": json_response}

    except Exception as e:
        error_message = f"Error al generar la respuesta: {str(e)}"
        print(error_message)  # Log del error en la consola
        raise HTTPException(status_code=500, detail=error_message)

# Ejecutar el servidor con:
# uvicorn server:app --host 0.0.0.0 --port 8000 --reload
