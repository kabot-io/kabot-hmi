# 201 Dynamic Port Assignment

The Next.js frontend communicates with the Python backend via WebSockets. Hardcoding the port (e.g., `8000`) is dangerous because the port might already be in use on the host machine, leading to crashes.

## Solution
1. **Rust Binding**: When Tauri starts (`lib.rs`), it binds a `std::net::TcpListener` to `"127.0.0.1:0"`. The OS automatically assigns a random, open port.
2. **Sidecar Environment Variable**: Rust extracts the assigned port number and sets it as an environment variable (`KABOT_BACKEND_PORT`) when spawning the [200 Tauri Sidecar Pattern](./200-tauri-sidecar-pattern.md).
3. **Frontend Retrieval**: The Next.js frontend requests the port from Tauri via the IPC bridge `invoke('get_backend_port')` before opening the WebSocket connection.
4. **Backend Bind**: The Python backend reads `os.environ.get("KABOT_BACKEND_PORT")` to start its FastAPI/uvicorn server.

---
#networking #ports #tauri #rust
