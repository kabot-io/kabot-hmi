# 100 Application Architecture

The `kabot-hmi` application uses a decoupled frontend-backend architecture packaged as a single executable desktop application via Tauri.

## Components
1. **Frontend**: Next.js (React) static web application. It serves the UI, Monaco Editor, and establishes WebSocket connections to the backend.
2. **Backend**: Python script (`main.py`) that handles robotic control state and translation over UDP.
3. **App Shell**: Tauri (Rust), which serves the UI, bundles the application into a Linux AppImage, and manages the execution lifecycle of the Python backend.

For details on how the backend and frontend are tied together by Tauri, see [200 Tauri Sidecar Pattern](./200-tauri-sidecar-pattern.md).

---
#architecture #nextjs #tauri #python
