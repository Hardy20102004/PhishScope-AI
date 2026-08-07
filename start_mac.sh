#!/bin/bash
# =====================================================================
#  PhishScope AI 2.0 — macOS Startup Script
#  Usage: chmod +x start_mac.sh && ./start_mac.sh
# =====================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo ""
echo "  ██████╗ ██╗  ██╗ ██████╗ ███████╗███╗   ██╗██╗██╗  ██╗"
echo "  ██╔══██╗██║  ██║██╔═══██╗██╔════╝████╗  ██║██║╚██╗██╔╝"
echo "  ██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║██║ ╚███╔╝ "
echo "  ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║██║ ██╔██╗ "
echo "  ██║     ██║  ██║╚██████╔╝███████╗██║ ╚████║██║██╔╝ ██╗"
echo "  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝"
echo "  PhishScope AI 2.0 — macOS Launcher"
echo ""

# ── Clear any stale processes on our ports ──────────────────────────
echo "  [1/4] Clearing ports 8000 & 3000..."
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
lsof -ti :3000 | xargs kill -9 2>/dev/null || true
sleep 1

# ── Backend ──────────────────────────────────────────────────────────
echo "  [2/4] Starting backend (FastAPI on :8000)..."
cd "$BACKEND_DIR"
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "         Backend PID: $BACKEND_PID"

# ── Wait for backend health ───────────────────────────────────────────
echo "  [3/4] Waiting for backend to be healthy..."
for i in {1..30}; do
  if curl -sf http://localhost:8000/api/v1/health/live > /dev/null 2>&1; then
    echo "         ✓ Backend healthy"
    break
  fi
  sleep 1
done

# ── Frontend ─────────────────────────────────────────────────────────
echo "  [4/4] Starting frontend (Vite on :3000)..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!
echo "         Frontend PID: $FRONTEND_PID"
sleep 3

echo ""
echo "  ┌────────────────────────────────────────────────────┐"
echo "  │  ✅  All systems operational!                       │"
echo "  │                                                     │"
echo "  │  Frontend   →  http://localhost:3000               │"
echo "  │  Backend    →  http://localhost:8000               │"
echo "  │  API Docs   →  http://localhost:8000/docs          │"
echo "  │                                                     │"
echo "  │  Admin Email    :  admin@phoenix.ai                │"
echo "  │  Admin Password :  Phoenix@Admin123                │"
echo "  │  ⚠  Change password after first login!            │"
echo "  └────────────────────────────────────────────────────┘"
echo ""
echo "  Press Ctrl+C to stop all services."
echo ""

# ── Trap Ctrl+C ──────────────────────────────────────────────────────
trap "echo ''; echo '  Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM

# Keep running
wait $BACKEND_PID $FRONTEND_PID
