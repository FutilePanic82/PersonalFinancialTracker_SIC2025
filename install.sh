#!/usr/bin/env bash
# ============================================================================
#  install.sh — Personal Financial Tracker · Interactive Installer
# ============================================================================
#  Usage: chmod +x install.sh && ./install.sh
# ============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/Backend&Algorithms"
FRONTEND_DIR="$ROOT_DIR/chatbot-angular"
VENV_DIR="$BACKEND_DIR/venv"

# ── Colors ─────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

# ── Helper Functions ───────────────────────────────────────────────────────
info() { echo -e "${CYAN}▸ $1${NC}"; }
ok()   { echo -e "${GREEN}✔ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }
fail() { echo -e "${RED}✖ $1${NC}"; exit 1; }
ask()  {
    local prompt="$1"
    local default="$2"
    local reply
    read -p "$(echo -e "${BOLD}$prompt${NC} [$default]: ")" reply
    echo "${reply:-$default}"
}

# ── Header ─────────────────────────────────────────────────────────────────
clear
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                ║${NC}"
echo -e "${CYAN}║   💰 Personal Financial Tracker — SIC 2025 Installer           ║${NC}"
echo -e "${CYAN}║                                                                ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Este script te guiará paso a paso para instalar las dependencias necesarias."
echo -e "Se realizarán comprobaciones de sistema y configuración de entorno."
echo ""

# ── DOCKER OPTION ──────────────────────────────────────────────────────────
DO_DOCKER=$(ask "🛠️  ¿Deseas instalar y ejecutar todo con DOCKER? (Recomendado para producción)" "N")

if [[ "$DO_DOCKER" =~ ^[Yy]$ ]]; then
    info "🐳 Iniciando instalación con Docker..."
    
    # Check Docker
    if ! command -v docker >/dev/null 2>&1; then
        fail "Docker no está instalado. Por favor instala Docker Desktop o Docker Engine."
    fi
    
    # Check Docker Compose (modern 'docker compose' or legacy 'docker-compose')
    if command -v docker-compose >/dev/null 2>&1; then
        DOCKER_COMPOSE_CMD="docker-compose"
    elif docker compose version >/dev/null 2>&1; then
        DOCKER_COMPOSE_CMD="docker compose"
    else
        fail "Docker Compose no encontrado."
    fi
    ok "Docker y Docker Compose detectados."

    # Ollama Check for Docker
    echo ""
    info "ℹ️  Para que Docker vea tu Ollama local, asegúrate de que Ollama esté corriendo."
    if ! pgrep ollama >/dev/null; then
        warn "Ollama NO está corriendo en el host. El backend en Docker podría fallar al conectar."
        echo -e "    Ejecuta 'ollama serve' en otra terminal antes de continuar."
        read -p "Presiona ENTER cuando Ollama esté listo..."
    else
        ok "Ollama está corriendo en el host."
    fi

    echo ""
    info "🚀 Construyendo y levantando contenedores..."
    $DOCKER_COMPOSE_CMD up --build -d
    
    echo ""
    echo -e "${GREEN}✅ DOCKER SETUP COMPLETADO${NC}"
    echo -e "   • Frontend: http://localhost:80"
    echo -e "   • Backend:  http://localhost:8000/docs"
    echo -e "   • Logs:     $DOCKER_COMPOSE_CMD logs -f"
    echo ""
    exit 0
fi

# ============================================================================
#  STANDARD INSTALLATION (LOCAL)
# ============================================================================

# ── 1. Check Prerequisites ─────────────────────────────────────────────────
info "🔍 Comprobando prerequisitos del sistema..."

# Python Check
if command -v python3 >/dev/null 2>&1; then
    PY_VER=$(python3 --version | awk '{print $2}')
    ok "Python detectado: $PY_VER"
else
    fail "Python3 no encontrado. Por favor instala Python 3.10 o superior."
fi

# Node Check
if command -v node >/dev/null 2>&1; then
    NODE_VER=$(node --version)
    ok "Node.js detectado: $NODE_VER"
else
    warn "Node.js no encontrado. El frontend no podrá instalarse."
fi

# NPM Check
if command -v npm >/dev/null 2>&1; then
    NPM_VER=$(npm --version)
    ok "NPM detectado: $NPM_VER"
else
    warn "NPM no encontrado."
fi

# Ollama Check
if command -v ollama >/dev/null 2>&1; then
    ok "Ollama detectado (necesario para modo local)"
else
    warn "Ollama no detectado. Si planeas usar LLM local, instálalo desde https://ollama.com"
fi

echo ""

# ── 2. Interactive Menu ───────────────────────────────────────────────────
DO_BACKEND=$(ask "Instalar dependencias del Backend (Python)?" "Y")
DO_FRONTEND=$(ask "Instalar dependencias del Frontend (Angular)?" "Y")
DO_LLM=$(ask "Configurar modelo LLM (Ollama)?" "Y")

# ── 3. Backend Installation ───────────────────────────────────────────────
if [[ "$DO_BACKEND" =~ ^[Yy]$ ]]; then
    echo ""
    info "📦 Instalando Backend..."
    
    if [ ! -d "$VENV_DIR" ]; then
        info "Creando entorno virtual en $VENV_DIR..."
        python3 -m venv "$VENV_DIR"
        ok "Entorno virtual creado."
    fi

    info "Activando entorno virtual..."
    source "$VENV_DIR/bin/activate"
    
    info "Instalando librerías desde requirements.txt..."
    # Using specific comments for key libraries
    echo -e "   • ${YELLOW}FastAPI & Uvicorn${NC}: Servidor web asíncrono."
    echo -e "   • ${YELLOW}Scikit-learn & Torch${NC}: Modelos de ML y IA."
    echo -e "   • ${YELLOW}Pandas & NumPy${NC}: Procesamiento de datos."
    echo -e "   • ${YELLOW}Ollama & OpenAI${NC}: Conectores LLM."
    
    pip install --upgrade pip -q
    pip install -r "$BACKEND_DIR/requirements.txt"
    
    ok "Dependencias de Backend instaladas correctamente."
else
    warn "Saltando instalación de Backend."
fi

# ── 4. Frontend Installation ──────────────────────────────────────────────
if [[ "$DO_FRONTEND" =~ ^[Yy]$ ]]; then
    echo ""
    info "🎨 Instalando Frontend..."
    
    if [ -d "$FRONTEND_DIR" ]; then
        cd "$FRONTEND_DIR"
        info "Ejecutando npm install..."
        npm install
        ok "Dependencias de Angular instaladas."
        cd "$ROOT_DIR"
    else
        fail "Directorio de frontend no encontrado en $FRONTEND_DIR"
    fi
else
    warn "Saltando instalación de Frontend."
fi

# ── 5. LLM Configuration ──────────────────────────────────────────────────
if [[ "$DO_LLM" =~ ^[Yy]$ ]]; then
    echo ""
    info "🤖 Configurando LLM..."
    
    if command -v ollama >/dev/null 2>&1; then
        LLM_MODEL="llama3.2:3b" # Default model
        info "Descargando modelo $LLM_MODEL..."
        ollama pull "$LLM_MODEL"
        ok "Modelo $LLM_MODEL listo."
        
        info "Iniciando servicio Ollama..."
        # Check if ollama is running
        if pgrep ollama >/dev/null; then
             ok "Ollama ya está en ejecución."
        else
             warn "Ollama no está corriendo. Recuerda ejecutar 'ollama serve' en otra terminal."
        fi
    else
        fail "Ollama no está instalado. No se puede configurar el modelo."
    fi
    
    # Configure .env if not exists
    if [ ! -f "$ROOT_DIR/.env" ]; then
        info "Creando archivo .env por defecto..."
        echo "LLM_MODE=ollama" > "$ROOT_DIR/.env"
        echo "LLM_MODEL=llama3.2:3b" >> "$ROOT_DIR/.env"
        ok "Archivo .env creado."
    fi
else
    warn "Saltando configuración LLM."
fi

# ── 6. Documentation & Summary ─────────────────────────────────────────────
echo ""
echo -e "${GREEN}✅ INSTALACIÓN COMPLETADA EXITOSAMENTE${NC}"
echo ""
echo -e "${CYAN}📚 DOCUMENTACIÓN RÁPIDA DE COMANDOS${NC}"
echo -e "===================================================================="
echo ""
echo -e "${BOLD}1. INICIAR TODO EL SISTEMA:${NC}"
echo -e "   ${GREEN}./start.sh${NC}"
echo -e "   (Arranca Backend, Frontend y Ollama automáticamente)"
echo ""
echo -e "${BOLD}2. DETENER SERVICIOS:${NC}"
echo -e "   ${GREEN}./stop.sh${NC}"
echo ""
echo -e "${BOLD}3. EJECUCIÓN MANUAL:${NC}"
echo -e "   ${CYAN}Backend API:${NC}"
echo -e "     cd \"Backend&Algorithms\""
echo -e "     source venv/bin/activate"
echo -e "     uvicorn server:app --reload"
echo -e "     👉 Swagger Docs: http://localhost:8000/docs"
echo ""
echo -e "   ${CYAN}Frontend Angular:${NC}"
echo -e "     cd chatbot-angular"
echo -e "     ng serve"
echo -e "     👉 UI: http://localhost:4200"
echo ""
echo -e "${BOLD}4. DOCUMENTACIÓN COMPLETA:${NC}"
echo -e "   Consulta el archivo README.md para detalles de endpoints y arquitectura."
echo ""
echo -e "===================================================================="
echo ""
