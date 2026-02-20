# 💰 Personal Financial Tracker — SIC 2025

Un asistente de finanzas personales impulsado por **Inteligencia Artificial** que te permite registrar tus ingresos y gastos mediante lenguaje natural. El sistema clasifica automáticamente tus transacciones utilizando **SVM + DistilBERT** y predice tu comportamiento de gasto mensual a través de **Regresión Polinómica**.

---

## ✨ Características Principales

| Módulo | Descripción |
| --- | --- |
| 💬 **Chatbot Conversacional** | Interacción fluida en lenguaje natural mediante LLMs (Ollama / LLaMA 3.2). Registra gastos e ingresos como si conversaras con un asesor humano. |
| 🤖 **Clasificación Inteligente** | Etiquetado automático de conceptos usando *embeddings* de DistilBERT y clasificación con el modelo SVM en tiempo real. |
| 📊 **Análisis y Predicción** | Panel interactivo con resumen por categoría y predicción avanzada de gasto mensual basada en Regresión Polinómica (Grado 2). |
| 🎯 **Metas Financieras** | Herramientas interactivas para distribuir tu presupuesto y recibir consejos personalizados y automatizados del asesor IA. |
| 🗄️ **Almacenamiento y Exportación**| Base de datos local en SQLite para consultar todo el historial y exportación rápida de transacciones a formato Excel (`.xlsx`). |

---

## 🛠️ Stack Tecnológico

- **Frontend:** Angular 17+ (Componentes Standalone).
- **Backend:** Python, FastAPI, Uvicorn.
- **Inteligencia Artificial (LLM):** Ollama ejecutando `llama3.2:3b`.
- **Machine Learning:** Scikit-learn (SVM, Regresión Polinómica) y Hugging Face Transformers (DistilBERT).
- **Base de Datos:** SQLite.
- **Procesamiento de Datos:** Pandas y XlsxWriter.

---

## 🚀 Guía de Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/FutilePanic82/PersonalFinancialTracker_SIC2025
cd PersonalFinancialTracker_SIC2025
```

### 2. Configuración del Backend (Python)
```bash
cd "Backend&Algorithms"
python -m venv venv

# Activar el entorno virtual:
source venv/bin/activate        # En macOS/Linux
# venv\Scripts\activate         # En Windows

pip install -r requirements.txt
```

### 3. Configurar Ollama (Motor LLM local)
Descarga e instala [Ollama](https://ollama.com/), luego ejecuta desde tu terminal:
```bash
ollama pull llama3.2:3b
ollama serve
```
*(Asegúrate de mantener este proceso activo en una terminal separada).*

### 4. Iniciar el Servidor Backend
En la misma carpeta `Backend&Algorithms` y con el entorno virtual activado, ejecuta:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Configuración del Frontend (Angular)
En una nueva terminal, navega a la carpeta de Angular, instala las dependencias e inicia el servidor de desarrollo:
```bash
cd chatbot-angular
npm install
ng serve
```
*Tu aplicación estará disponible en el navegador accediendo a: [http://localhost:4200](http://localhost:4200)*

---

## 📡 Referencia de la API

El Backend expone una API REST moderna con los siguientes endpoints principales:

| Método | Endpoint | Acción |
| --- | --- | --- |
| `POST` | `/conversation` | Envía un mensaje en texto plano para que sea analizado, y clasifica las transacciones extraídas. |
| `GET` | `/historial` | Obtiene el registro completo de transacciones almacenadas en SQLite. |
| `POST` | `/finalize` | Genera y descarga de forma local un archivo `.xlsx` con todas las transacciones. |
| `POST` | `/predict` | Realiza una predicción del gasto futuro usando modelos de regresión basándose en tus datos. |
| `POST` | `/metas` | Evalúa la distribución del presupuesto seleccionado para retornar consejos estratégicos de la IA. |
| `DELETE` | `/reset` | Borra en memoria el historial de la conversación actual. |

### Ejemplos de uso (API REST)

<details>
<summary><b>Ejemplo: POST <code>/conversation</code></b></summary>

**Request:**
```json
{
  "chat_history": [
    { "role": "user", "content": "Gasté $500 en comida y recibí $15000 de sueldo" }
  ]
}
```

**Response:**
```json
{
  "response": "He registrado tu gasto de $500 en comida y tu ingreso de $15,000.",
  "transacciones_detectadas": [
    { "concepto": "comida", "monto": 500, "categoria": "Alimentación", "tipo": "gasto" },
    { "concepto": "sueldo", "monto": 15000, "categoria": "Ingresos", "tipo": "ingreso" }
  ]
}
```
</details>

<details>
<summary><b>Ejemplo: POST <code>/predict</code></b></summary>

**Request:**
```json
{ "ingresos": 15000, "hijos": 1, "edad": 30, "educacion": 2 }
```

**Response:**
```json
{
  "gasto_predicho": 11250.50,
  "r2": 0.8724,
  "ahorro_estimado": 3749.50
}
```
</details>

---

## 🏗️ Arquitectura del Proyecto

<details>
<summary><b>Ver estructura comprimida del repositorio</b></summary>

Para facilitar su mantenimiento, el proyecto está segmentado de forma modular:

```text
PersonalFinancialTracker_SIC2025/
├── Backend&Algorithms/
│   ├── classifier.py         # Lógica central del ML (Clasificación SVM + DistilBERT)
│   ├── database.py           # Funcionalidades del gestor SQLite
│   ├── llm_provider.py       # Abstracción y proveedor de los LLMs
│   ├── predictor.py          # Modelo predictivo (Regresión lineal/polinómica)
│   ├── server.py             # Instancia principal del servidor FastAPI
│   └── ...                   # Modelos pre-entrenados .pkl scripts de base de datos
├── chatbot-angular/
│   ├── src/app/              # Base y UI orientada a componentes Angular
│   │   ├── analisis-gastos/  # Panel de gráficos
│   │   ├── chatbot/          # Vista del hub conversacional
│   │   ├── historial/        # Datatable de visualización
│   │   └── metas-financieras/# Sliders interactivos
│   └── ...                   # Configuración del frontend y dependencias node
├── Dockerfile & docker-compose.yml 
├── setup.sh & start.sh       # Scripts de automatización y despliegue rápido
└── ...
```
</details>

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Eres libre de usarlo, modificarlo y distribuirlo de acuerdo con los términos de dicha licencia.
