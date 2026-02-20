#!/usr/bin/env bash
# ============================================================================
#  setup.sh — Personal Financial Tracker · First-time setup
# ============================================================================
#  Run once:  chmod +x setup.sh && ./setup.sh
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

ok()   { echo -e "${GREEN}✔ $1${NC}"; }
info() { echo -e "${CYAN}▸ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }
fail() { echo -e "${RED}✖ $1${NC}"; exit 1; }

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   💰 Personal Financial Tracker — Setup             ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# ── 1. Check prerequisites ──────────────────────────────────────────────────
info "Checking prerequisites..."

command -v python3 >/dev/null 2>&1 || fail "python3 not found. Install Python 3.10+"
command -v node    >/dev/null 2>&1 || fail "node not found. Install Node.js 18+"
command -v npm     >/dev/null 2>&1 || fail "npm not found. Install Node.js 18+"
command -v ollama  >/dev/null 2>&1 || fail "ollama not found. Install from https://ollama.com"

ok "python3 $(python3 --version 2>&1 | awk '{print $2}')"
ok "node    $(node --version)"
ok "npm     $(npm --version)"
ok "ollama  found"

# ── 2. Python virtual environment ───────────────────────────────────────────
echo ""
info "Setting up Python virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    ok "Virtual environment created at $VENV_DIR"
else
    ok "Virtual environment already exists"
fi

source "$VENV_DIR/bin/activate"
ok "Virtual environment activated"

info "Installing Python dependencies (this may take a few minutes)..."
pip install --upgrade pip -q
pip install -r "$BACKEND_DIR/requirements.txt" -q
ok "Python dependencies installed"

# ── 3. Ollama — pull model ──────────────────────────────────────────────────
echo ""
info "Pulling Ollama model llama3.2:3b (skip if already pulled)..."
ollama pull llama3.2:3b
ok "Ollama model llama3.2:3b ready"

# ── 4. Angular frontend dependencies ────────────────────────────────────────
echo ""
info "Installing Angular frontend dependencies..."

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    (cd "$FRONTEND_DIR" && npm install)
    ok "Angular dependencies installed"
else
    ok "Angular node_modules already present"
fi

# ── 5. Summary ──────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅  Setup complete!                                ║${NC}"
echo -e "${GREEN}║                                                      ║${NC}"
echo -e "${GREEN}║   Next steps:                                        ║${NC}"
echo -e "${GREEN}║     ./start.sh   — Launch the full stack             ║${NC}"
echo -e "${GREEN}║     ./stop.sh    — Stop all services                 ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""
