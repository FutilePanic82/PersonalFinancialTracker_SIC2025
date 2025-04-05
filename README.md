# PersonalFinancialTracker_SIC2025
# Chatbot de Finanzas Personales

Este proyecto es un chatbot basado en FastAPI y Ollama, diseñado para ayudar a los usuarios a organizar sus finanzas personales. El chatbot interactúa con los usuarios, clasifica ingresos y gastos en categorías específicas y genera un archivo Excel con los datos recopilados.

## Características
- Interacción en tiempo real a través de una API REST.
- Clasificación automática de ingresos y gastos mediante un modelo de Machine Learning.
- Generación de un archivo Excel con el historial financiero del usuario.
- Implementación de CORS para permitir peticiones desde un frontend en Angular.

## Tecnologías Utilizadas
- **Backend:** FastAPI (Python)
- **Modelo de lenguaje:** Ollama con el modelo `llama3.2:3b`
- **Procesamiento de datos:** Pandas, JSON
- **Generación de Excel:** XlsxWriter
- **Frontend:** Angular (ubicado en un repositorio separado)

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/FutilePanic82/PersonalFinancialTracker_SIC2025
```

### 2. Crear un Entorno Virtual (Opcional pero Recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar Ollama y Descargar el Modelo
Ollama debe estar en ejecución y el modelo `llama3.2:3b` debe estar disponible. Si no lo tienes, descárgalo con:
```bash
ollama pull llama3.2:3b
```

### 5. Ejecutar el Servidor
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints de la API

### 1. Conversación con el Chatbot
**Endpoint:** `POST /conversation`

**Ejemplo de solicitud:**
```json
{
  "chat_history": [
    {"role": "user", "content": "Gané 5000 este mes y gasté 2000 en comida."}
  ]
}
```

**Ejemplo de respuesta:**
```json
{
  "response": "Entiendo, he registrado tus ingresos y gastos."
}
```

### 2. Generar Archivo Excel
**Endpoint:** `POST /finalize`

**Ejemplo de solicitud:**
```json
{
  "chat_history": []
}
```

**Respuesta:** Archivo Excel generado con los datos organizados.

## Errores Comunes y Soluciones

### 1. `model "llama3.2:3b" not found`
- Asegúrate de haber descargado el modelo con `ollama pull llama3.2:3b`.
- Verifica que Ollama está en ejecución.

### 2. `El LLM devolvió una respuesta no válida en JSON`
- Revisa los logs del servidor (`logs/server.log`) para ver la respuesta completa del LLM.
- Asegúrate de que el historial de chat tenga contexto suficiente antes de llamar a `/finalize`.

## Contribuciones
Si deseas contribuir, abre un issue o un pull request en el repositorio. Apreciamos cualquier mejora en el código o documentación.

## Licencia
Este proyecto está bajo la Licencia MIT.

