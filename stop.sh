#!/usr/bin/env bash
# ============================================================================
#  stop.sh — Personal Financial Tracker · Stop all services
# ============================================================================
#  Usage:  ./stop.sh
# ============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$ROOT_DIR/.pids"

# ── Colors ─────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✔ $1${NC}"; }
info() { echo -e "${CYAN}▸ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   🛑 Personal Financial Tracker — Stop              ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

kill_proc() {
    local name="$1"
    local pid="$2"

    if [ "$pid" = "external" ]; then
        info "$name was running externally — not stopping it"
        return
    fi

    if kill -0 "$pid" 2>/dev/null; then
        kill "$pid" 2>/dev/null || true
        # Wait up to 5 seconds for graceful shutdown
        for i in $(seq 1 10); do
            if ! kill -0 "$pid" 2>/dev/null; then
                break
            fi
            sleep 0.5
        done
        # Force kill if still alive
        if kill -0 "$pid" 2>/dev/null; then
            kill -9 "$pid" 2>/dev/null || true
            warn "$name (PID $pid) force-killed"
        else
            ok "$name (PID $pid) stopped"
        fi
    else
        info "$name (PID $pid) already stopped"
    fi
}

if [ -f "$PID_FILE" ]; then
    source "$PID_FILE"

    kill_proc "Frontend"  "${FRONTEND_PID:-}"
    kill_proc "Backend"   "${BACKEND_PID:-}"
    kill_proc "Ollama"    "${OLLAMA_PID:-}"

    rm -f "$PID_FILE"
    ok "PID file cleaned up"
else
    warn "No PID file found — trying to kill by port..."

    # Kill processes on known ports as fallback
    for port in 4200 8000; do
        pid=$(lsof -ti :$port 2>/dev/null || true)
        if [ -n "$pid" ]; then
            kill $pid 2>/dev/null || true
            ok "Killed process on port $port (PID $pid)"
        fi
    done
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅ All services stopped.                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""
