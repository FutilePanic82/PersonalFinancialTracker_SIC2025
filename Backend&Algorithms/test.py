from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
from fastapi.middleware.cors import CORSMiddleware
import re
from transformers import BertTokenizer, BertModel
import torch

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

# Historial de conversación
chat_history = []

# Modelo de datos para la solicitud
class PromptRequest(BaseModel):
    prompt: str

def procesar_con_bert(texto):
    """
    Convierte el texto en un vector numérico usando BERT.
    :param texto: Concepto de gasto extraído por el LLM.
    :return: Tensor de representación numérica.
    """
    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy().tolist()  # Extraer embedding del CLS token

@app.post("/generate")
def generate_response(request: PromptRequest):
    global chat_history

    try:
        # Agregar la entrada del usuario al historial
        chat_history.append({"role": "user", "content": request.prompt})

        # Llamar a Ollama para filtrar solo el concepto de gasto
        response = ollama.chat(
            model="llama3.2:3b",
            messages=chat_history
        )

        # Extraer la respuesta del modelo
        raw_response = response["message"]["content"]
        cleaned_response = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()

        # Agregar la respuesta filtrada al historial
        chat_history.append({"role": "assistant", "content": cleaned_response})

        # Convertir el concepto a representación numérica con BERT
        embedding = procesar_con_bert(cleaned_response)

        return {"concepto": cleaned_response, "vector": embedding}

    except Exception as e:
        error_message = f"Error al generar la respuesta: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

