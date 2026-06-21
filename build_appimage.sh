#!/usr/bin/env bash

set -e

# Change to project root
cd "$(dirname "$0")"

echo "=== Building Python Backend ==="
cd backend
# Make sure the script is executable
chmod +x build_backend.sh
./build_backend.sh

echo "=== Moving sidecar binary to Tauri directories ==="
cd ..
mkdir -p frontend/src-tauri/binaries

# Tauri v2 requires sidecar binaries to be suffixed with the target triple
# e.g., x86_64-unknown-linux-gnu or aarch64-unknown-linux-gnu.
# Let's get the rust target triple:
TARGET_TRIPLE=$(rustc -vV | sed -n 's|host: ||p')
cp backend/dist/kabot_backend "frontend/src-tauri/binaries/kabot_backend-${TARGET_TRIPLE}"

echo "=== Building Next.js Frontend ==="
cd frontend
npm install
npm run build

echo "=== Building Tauri AppImage ==="
if [ -f "$HOME/.cargo/env" ]; then
    source "$HOME/.cargo/env"
fi
npx tauri build

echo "=== Build Complete ==="
rm -f ../*.AppImage
cp src-tauri/target/release/bundle/appimage/*.AppImage ../
echo "AppImage copied to $(dirname $(pwd))"
echo "You can find your AppImage in frontend/src-tauri/target/release/bundle/appimage/"
