#!/usr/bin/env bash

set -e

# Change to the backend directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Install pyinstaller if not already installed
pip install pyinstaller

# Build the standalone executable
pyinstaller --onefile --name kabot_backend \
  --add-data "state_control_msg.proto:." \
  main.py

echo "Build complete. Executable is at dist/kabot_backend"
