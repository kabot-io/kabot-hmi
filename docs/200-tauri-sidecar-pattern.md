# 200 Tauri Sidecar Pattern

To ship both a Next.js frontend and a Python backend as a single desktop app without requiring the user to install Python, `kabot-hmi` uses the **Tauri Sidecar Pattern**.

## How it works
1. The Python script is compiled into a standalone binary using [300 Python Packaging with PyInstaller](./300-python-packaging-pyinstaller.md).
2. The standalone binary is moved to `frontend/src-tauri/binaries/kabot_backend-<target_triple>`.
3. In `tauri.conf.json`, `externalBin: ["binaries/kabot_backend"]` tells Tauri to embed this binary in the final build.
4. On startup, Tauri's Rust entry point (`lib.rs`) spawns the binary as a child process.

## Process Lifecycle Management
If the Tauri app crashes or is closed, the sidecar process might be left running in the background. We solve this by implementing the Rust `Drop` trait on a struct holding the `CommandChild`, guaranteeing it is killed on exit. This prevents issues described in [301 UDP Socket Reuse & Orphan Cleanup](./301-udp-socket-reuse.md).

---
#tauri #sidecar #rust #process-management
