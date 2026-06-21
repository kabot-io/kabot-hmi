# 300 Python Packaging with PyInstaller

To eliminate the need for end-users to install Python, `kabot-hmi` uses PyInstaller to bundle the backend scripts into a standalone executable.

## The Build Process
1. A Python `venv` is created and dependencies are installed via `pip install -r requirements.txt`.
2. PyInstaller traces imports in `main.py` and bundles the CPython interpreter and all packages into a single binary.
3. For custom data files (like `.proto` buffers), `--add-data "state_control_msg.proto:."` ensures the file is accessible at runtime via PyInstaller's ephemeral `_MEIPASS` directory.

The master build script `build_appimage.sh` handles this compilation before feeding the resulting binary to the Tauri build process described in [200 Tauri Sidecar Pattern](./200-tauri-sidecar-pattern.md).

---
#python #pyinstaller #packaging #build
