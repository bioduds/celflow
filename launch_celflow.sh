#!/bin/bash

# CelFlow System Launcher Wrapper
# This wrapper calls the actual launch script in backend/scripts/

exec "$(dirname "$0")/backend/scripts/launch_celflow.sh" "$@" 