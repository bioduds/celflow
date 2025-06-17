#!/bin/bash

# CelFlow Desktop Launcher
# This script directly launches the CelFlow desktop app

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

echo "Launching CelFlow Desktop..."

# Navigate to desktop directory
cd frontend/desktop

# Launch Tauri app
echo "Starting Tauri desktop app..."
npm run tauri:dev -- --no-watch

echo "Desktop app exited." 