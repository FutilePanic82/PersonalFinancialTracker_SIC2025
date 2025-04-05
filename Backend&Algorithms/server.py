from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
from fastapi.middleware.cors import CORSMiddleware
import re  

app = FastAPI()

# Permitir CORS para Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Ajusta si Angular está en otro dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prompt global (se usa solo al inicio)
global_prompt = {
    "role": "system",
    "content": "Eres un agente especializado en finanzas personales. Responde solo en español. Tu objetivo es generar un archivo Excel con los gastos mensuales del usuario. Debes hacer preguntas hasta obtener toda la información necesaria y hacerlas una a una. Si es tu primera interaccion"
    "deberas comenzar preguntando por su ingreso mensual, todos los meses deberas preguntar si recibio algun ingreso extra, deberas de confirmar si termino de ingresar sus ingresos,"
    "despues de terminar con sus ingresos deberas con sus gastos fijos mensuales en la primera interaccion, si no es la primera se los deberas mostrar y preguntarle si los confirma."
    "Despues de terminar con los gastos fijos deberas preguntarle acerca de sus gastos uno a uno de ese mes hasta que el usuario confirme de no mas gastos. Una vez concluido estos pasos "
    "deberas generar el archivo excel."
    "Si necesitas preguntar acerca de algo no olvides que debes esperar la respuesta del usaurio, Siempre debes hacer preguntas que devuelvan solamente una respuesta. Haz preguntas especificas"
    "y si dudas de algo pregunta hasta estar mas de 90 por ciento seguro."
    "Extrae solo el concepto de gasto o ingreso de las entradas del usuario y devuélvelo sin información adicional, si no hay informacion relevante "
}

# Historial de conversación
chat_history = []

# Modelo de datos para la solicitud
class PromptRequest(BaseModel):
    prompt: str

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

        return {"response": cleaned_response}

    except Exception as e:
        error_message = f"Error al generar la respuesta: {str(e)}"
        print(error_message)  # Log del error en la consola
        raise HTTPException(status_code=500, detail=error_message)

# Ejecutar el servidor con:
# uvicorn server:app --host 0.0.0.0 --port 8000 --reload
