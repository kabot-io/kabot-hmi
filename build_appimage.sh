#!/usr/bin/env bash

set -e

# Change to project root
cd "$(dirname "$0")"

# Automatically update version based on Git tags
python3 << 'EOF'
import json, subprocess, re

try:
    desc = subprocess.check_output(['git', 'describe', '--tags', '--always']).decode().strip()
    desc = desc.lstrip('v')
    if '-' in desc:
        base = desc.split('-')[0]
        ver = f"{base}-next"
    else:
        ver = desc

    print(f"=== Auto-updating version to {ver} ===")

    def update_json(path, field, value):
        with open(path, 'r') as f:
            data = json.load(f)
        data[field] = value
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    update_json('frontend/package.json', 'version', ver)
    update_json('frontend/src-tauri/tauri.conf.json', 'version', ver)

    with open('frontend/src-tauri/Cargo.toml', 'r') as f:
        cargo = f.read()
    cargo = re.sub(r'^version\s*=\s*".*"', f'version = "{ver}"', cargo, count=1, flags=re.MULTILINE)
    with open('frontend/src-tauri/Cargo.toml', 'w') as f:
        f.write(cargo)
except Exception as e:
    print(f"Failed to auto-update version: {e}")
EOF


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
