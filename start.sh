#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo "Stopping servers..."
    if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        kill "$BACKEND_PID"
    fi
    if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        kill "$FRONTEND_PID"
    fi
}

trap cleanup SIGINT SIGTERM EXIT

echo "Bootstrapping backend environment..."
if [[ ! -d "$BACKEND_DIR/venv" ]]; then
    python3 -m venv "$BACKEND_DIR/venv"
fi

source "$BACKEND_DIR/venv/bin/activate"
python -m pip install --upgrade pip >/dev/null
python -m pip install -r "$BACKEND_DIR/requirements.txt" >/dev/null

echo "Bootstrapping frontend dependencies..."
if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
    (cd "$FRONTEND_DIR" && npm install)
fi

echo "Starting FastAPI Backend..."
(cd "$BACKEND_DIR" && python3 main.py) &
BACKEND_PID=$!

echo "Starting Next.js Frontend..."
(cd "$FRONTEND_DIR" && npm run dev) &
FRONTEND_PID=$!

echo "Servers are running! Access the frontend at http://localhost:3000"
echo "Press Ctrl+C to stop."
wait
