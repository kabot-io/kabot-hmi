# 500 GitHub Actions & AppImage

To distribute `kabot-hmi` to end-users easily, we fully automated the Linux AppImage creation process using a GitHub Actions CI/CD pipeline.

## Build Requirements
Building Tauri on Linux requires specific system dependencies that are baked into the GitHub Actions runner `ubuntu-22.04` via `apt-get`:
- `libwebkit2gtk-4.1-dev`
- `libgtk-3-dev`
- `libayatana-appindicator3-dev`
- `librsvg2-dev`

We also rely on `python3-venv` to dynamically create the virtual environment for PyInstaller during the build.

## Workflow Overview
Located at `.github/workflows/build-appimage.yml`, the automated pipeline performs the following steps:
1. Provisions Rust, Node.js, and Python environments.
2. Executes the `build_appimage.sh` master script.
3. Automatically attaches the generated `.AppImage` to the workflow run as a downloadable artifact for every push to `main`.
4. If the push is a Git Tag (e.g., `v1.0.0`), the workflow uses `softprops/action-gh-release@v2` to automatically publish a GitHub Release with the bundled AppImage attached.

---
#cicd #github-actions #appimage #packaging #tauri
