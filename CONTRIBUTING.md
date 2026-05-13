# Contribuir a PersonalFinancialTracker

## Setup del entorno de desarrollo

### Prerrequisitos
- Node.js 20+
- Python 3.10+
- Docker y Docker Compose (para desarrollo con contenedores)
- Ollama (para LLM local, opcional)

### Instalación

```bash
# Frontend (Angular)
cd chatbot-angular
npm install

# Backend (Python)
cd Backend&Algorithms
pip install -r requirements.txt

# Variables de entorno
cp .env.example .env  # editar segun necesidad
```

### Scripts disponibles

```bash
# Frontend
npm start          # Iniciar servidor de desarrollo (Angular CLI)
npm test           # Ejecutar tests (Karma/Jasmine)
npm run lint       # ESLint
npm run build      # Production build

# Backend
python server.py   # Iniciar servidor FastAPI
pytest             # Ejecutar tests Python

# Docker
docker-compose up  # Iniciar todos los servicios
./start.sh         # Script de inicio rapido
```

## Convenciones de código

### Angular / TypeScript
- Componentes standalone (sin NgModules)
- Prefijo `app-` para selectores de componentes
- Types para todos los inputs/outputs (evitar `any`)
- OnPush change detection strategy

### Python
- Ruff para linting y formateo
- Pydantic models para validación de inputs
- Docstrings para todas las funciones públicas

### Commits
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` documentación
- `refactor:` refactorización sin cambio de comportamiento
- `test:` agregar o modificar tests

## Testing

```bash
# Frontend
ng test --watch=false  # single run

# Backend
pytest -v
```

## Pull Requests

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/mi-feature`
3. Commit tus cambios: `git commit -m "feat: descripcion"`
4. Push a la rama: `git push origin feature/mi-feature`
5. Abre un Pull Request con descripción clara

## Reportar Issues

Usa la plantilla de bug report. Incluye:
- Pasos para reproducir
- Comportamiento esperado vs actual
- Stack trace o logs si aplica