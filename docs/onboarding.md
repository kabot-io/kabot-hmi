# Onboarding

## What this project is

This repository contains a web-based HMI mockup for Kabot robotics workflows.

- Backend: FastAPI + UDP + protobuf.
- Frontend: Next.js app with scope/plot tools and Python code editor.
- Transport:
  - UDP state ingress on port `30011`.
  - UDP control egress on port `30010`.
  - Browser/backend bridge over WebSocket at `/ws`.

## Prerequisites

- Linux/macOS shell environment.
- Python 3.10+ (`python3`).
- Node.js 20+ and npm.

## First run

From repo root:

```bash
./start.sh
```

`start.sh` now bootstraps dependencies automatically:

- Creates `backend/venv` when missing.
- Installs backend requirements into `backend/venv`.
- Installs frontend npm dependencies when missing.
- Starts backend and frontend together.
- Cleans up both processes on Ctrl+C.

## Where to open

- Frontend: usually `http://localhost:3000`.
- If `3000` is occupied, Next.js picks the next port (for example `3001`).
- Backend: `http://localhost:8000`.

## Current operator behaviors

- Scope view includes compact manual controls.
- Arrow controls map to effort values:
  - forward: `1, 1`
  - backward: `-1, -1`
  - left: `-1, 1`
  - right: `1, -1`
- Manual control target IP is configurable in the scope toolbar.
- Default control target IP is `172.20.10.2`.

## Key folders

- `backend/` - UDP/protobuf bridge and execution runtime.
- `frontend/` - Next.js UI.
- `docs/` - onboarding and architecture docs.

## Useful files to inspect first

- `backend/main.py`
- `backend/models.py`
- `backend/state_control_msg.proto`
- `backend/state_control_msg_pb2.py`
- `frontend/src/app/page.tsx`
- `frontend/src/components/ui/UPlotScope.tsx`
