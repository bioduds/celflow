#!/bin/bash

# CelFlow Launch Script
# This script manages the CelFlow system components

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Function to check if a process is running
check_process() {
    local pid_file=$1
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null; then
            return 0  # Process is running
        fi
    fi
    return 1  # Process is not running
}

# Function to stop a process
stop_process() {
    local pid_file=$1
    local process_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null; then
            echo "Stopping $process_name (PID: $pid)..."
            kill "$pid"
            sleep 2
            if ps -p "$pid" > /dev/null; then
                echo "Force stopping $process_name..."
                kill -9 "$pid"
            fi
        fi
        rm -f "$pid_file"
    fi
}

# Function to check Tauri dependencies
check_tauri_deps() {
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "Node.js is not installed. Please install it first."
        return 1
    fi

    # Check npm
    if ! command -v npm &> /dev/null; then
        echo "npm is not installed. Please install it first."
        return 1
    fi

    # Check Rust
    if ! command -v rustc &> /dev/null; then
        echo "Rust is not installed. Please install it first."
        return 1
    fi

    # Check Tauri CLI
    if ! cargo tauri --version &> /dev/null; then
        echo "Tauri CLI is not installed. Installing..."
        cargo install tauri-cli
        if [ $? -ne 0 ]; then
            echo "Failed to install Tauri CLI"
            return 1
        fi
    fi

    return 0
}

# Function to start the Tauri tray
start_tauri_tray() {
    echo "Starting Tauri tray..."
    
    # Check dependencies
    if ! check_tauri_deps; then
        echo "Missing Tauri dependencies. Please install them first."
        return 1
    fi
    
    # Kill any processes using port 3000
    echo "Freeing port 3000..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    
    # Start the Tauri tray
    cd frontend/desktop
    echo "Launching desktop app - please wait..."
    npm run tauri:dev -- --no-watch > /dev/null 2>&1 &
    echo $! > "$SCRIPT_DIR/tauri_tray.pid"
    cd "$SCRIPT_DIR"
    
    # Give it more time to initialize (desktop app needs more time)
    echo "Waiting for desktop app to initialize (5 seconds)..."
    sleep 5
    
    echo "Tauri tray and desktop app started"
}

# Function to start the system tray icon separately
start_system_tray() {
    echo "Starting system tray icon..."
    
    # Start the Python-based system tray
    python3 backend/scripts/launch_tauri_tray.py > /dev/null 2>&1 &
    echo $! > "$SCRIPT_DIR/system_tray.pid"
    
    echo "System tray icon started"
}

# Function to start the main system
start_main() {
    echo "Starting main system..."
    python3 backend/scripts/celflow.py > /dev/null 2>&1 &
    echo $! > main_system.pid
    echo "Main system started"
}

# Function to stop all components
stop_all() {
    echo "Stopping CelFlow components..."
    
    # Stop Tauri tray
    stop_process "tauri_tray.pid" "Tauri tray"
    
    # Stop system tray
    stop_process "system_tray.pid" "System tray"
    
    # Stop main system
    stop_process "main_system.pid" "Main system"
    
    # Kill any remaining processes
    echo "Cleaning up any remaining processes..."
    pkill -f "python.*$SCRIPT_DIR"
    pkill -f "tauri dev"
    pkill -f "npm run tauri"
    pkill -f "node.*tauri"
    pkill -f "CelFlow Desktop"
    
    echo "All components stopped"
}

# Function to start all components
start_all() {
    echo "Starting CelFlow..."
    
    # Start Tauri tray first
    start_tauri_tray
    
    # Start system tray icon
    start_system_tray
    
    # Give it a moment to initialize
    echo "Waiting for desktop app to initialize..."
    sleep 2
    
    # Start main system
    start_main
    
    echo "CelFlow started"
    
    # Show running processes
    echo -e "\nRunning processes:"
    ps aux | grep -E "python.*$SCRIPT_DIR|tauri" | grep -v grep
}

# Function to restart the system
restart_system() {
    echo "Restarting CelFlow..."
    stop_all
    sleep 2
    start_all
}

# Command processing
case "$1" in
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    restart)
        restart_system
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0 