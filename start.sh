#!/usr/bin/env bash
# ============================================================================
#  start.sh — Personal Financial Tracker · Launch all services
# ============================================================================
#  Usage:  ./start.sh
#  Starts:  Ollama → Backend (FastAPI) → Frontend (Angular)
#  PID file: .pids  (used by stop.sh)
# ============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/Backend&Algorithms"
FRONTEND_DIR="$ROOT_DIR/chatbot-angular"
VENV_DIR="$BACKEND_DIR/venv"
PID_FILE="$ROOT_DIR/.pids"
LOG_DIR="$ROOT_DIR/.logs"

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

# ── Pre-flight checks ──────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   💰 Personal Financial Tracker — Start             ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

[ -d "$VENV_DIR" ] || fail "Virtual environment not found. Run ./setup.sh first."

# Stop any previously running instances
if [ -f "$PID_FILE" ]; then
    warn "Found previous PID file, cleaning up..."
    bash "$ROOT_DIR/stop.sh" 2>/dev/null || true
fi

mkdir -p "$LOG_DIR"

# ── 1. Ollama ───────────────────────────────────────────────────────────────
info "Starting Ollama server..."

# Check if ollama is already serving
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    ok "Ollama already running on :11434"
    OLLAMA_PID="external"
else
    ollama serve > "$LOG_DIR/ollama.log" 2>&1 &
    OLLAMA_PID=$!
    # Wait for ollama to be ready
    for i in $(seq 1 15); do
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            break
        fi
        sleep 1
    done
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        ok "Ollama started (PID $OLLAMA_PID) — :11434"

        # Check for model existence and pull if missing
        if ! ollama list | grep -q "llama3.2:3b"; then
            info "Model llama3.2:3b not found. Pulling now..."
            ollama pull llama3.2:3b
            ok "Model llama3.2:3b pulled"
        fi
    else
        warn "Ollama may still be starting — check $LOG_DIR/ollama.log"
    fi
fi

# ── 2. Backend (FastAPI + Uvicorn) ──────────────────────────────────────────
info "Starting Backend (FastAPI on :8000)..."

source "$VENV_DIR/bin/activate"
cd "$BACKEND_DIR"
uvicorn server:app --host 0.0.0.0 --port 8000 --reload > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd "$ROOT_DIR"

# Wait for backend health
for i in $(seq 1 20); do
    if curl -s http://localhost:8000/docs >/dev/null 2>&1; then
        break
    fi
    sleep 1
done
if curl -s http://localhost:8000/docs >/dev/null 2>&1; then
    ok "Backend started (PID $BACKEND_PID) — http://localhost:8000"
else
    warn "Backend may still be loading models — check $LOG_DIR/backend.log"
    ok "Backend process launched (PID $BACKEND_PID)"
fi

# ── 3. Frontend (Angular) ──────────────────────────────────────────────────
info "Starting Frontend (Angular on :4200)..."

cd "$FRONTEND_DIR"
npx ng serve --host 0.0.0.0 > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd "$ROOT_DIR"

# Wait for Angular to compile
for i in $(seq 1 30); do
    if curl -s http://localhost:4200 >/dev/null 2>&1; then
        break
    fi
    sleep 2
done
if curl -s http://localhost:4200 >/dev/null 2>&1; then
    ok "Frontend started (PID $FRONTEND_PID) — http://localhost:4200"
else
    warn "Frontend may still be compiling — check $LOG_DIR/frontend.log"
    ok "Frontend process launched (PID $FRONTEND_PID)"
fi

# ── Save PIDs ───────────────────────────────────────────────────────────────
cat > "$PID_FILE" <<EOF
OLLAMA_PID=$OLLAMA_PID
BACKEND_PID=$BACKEND_PID
FRONTEND_PID=$FRONTEND_PID
EOF

# ── Done ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   🚀 All services are running!                      ║${NC}"
echo -e "${GREEN}║                                                      ║${NC}"
echo -e "${GREEN}║   🌐 Frontend:  http://localhost:4200                ║${NC}"
echo -e "${GREEN}║   ⚙️  Backend:   http://localhost:8000                ║${NC}"
echo -e "${GREEN}║   📄 API Docs:  http://localhost:8000/docs           ║${NC}"
echo -e "${GREEN}║   🤖 Ollama:    http://localhost:11434               ║${NC}"
echo -e "${GREEN}║                                                      ║${NC}"
echo -e "${GREEN}║   To stop:  ./stop.sh                               ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Logs are in .logs/ directory:${NC}"
echo "  tail -f .logs/backend.log"
echo "  tail -f .logs/frontend.log"
echo "  tail -f .logs/ollama.log"
echo ""
