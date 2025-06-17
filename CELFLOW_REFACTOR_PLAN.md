# CelFlow Refactor Plan - SelFlow → CelFlow

## Overview
Complete refactor from SelFlow to CelFlow for commercial launch with celflow.com domain.

## Refactor Mapping
- `SelFlow` → `CelFlow` (title case)
- `selflow` → `celflow` (lowercase)
- `selFlow` → `celFlow` (camelCase)
- `SELFLOW` → `CELFLOW` (uppercase)

## Files to Rename
### Root Level
- `launch_selflow.sh` → `launch_celflow.sh`

### Backend Scripts
- `backend/scripts/launch_selflow.sh` → `backend/scripts/launch_celflow.sh`
- `backend/scripts/run_selflow_live.py` → `backend/scripts/run_celflow_live.py`
- `backend/scripts/run_visual_selflow.py` → `backend/scripts/run_visual_celflow.py`
- `backend/scripts/selflow.py` → `backend/scripts/celflow.py`
- `backend/scripts/selflow_tray.py` → `backend/scripts/celflow_tray.py`

### Tools
- `tools/selflow_dashboard.py` → `tools/celflow_dashboard.py`
- `tools/selflow_events.py` → `tools/celflow_events.py`

### Environment
- `environments/selflow_env/` → `environments/celflow_env/`

### Log Files
- `logs/selflow_*.log` → `logs/celflow_*.log`
- `logs/selflow_*.pid` → `logs/celflow_*.pid`

### Data Files
- `data/selflow_events.db` → `data/celflow_events.db`

### TypeScript Types
- `frontend/desktop/src/types/selflow.ts` → `frontend/desktop/src/types/celflow.ts`

## Content Changes
### Package Configuration
- `pyproject.toml`: name, URLs, entry points
- `frontend/desktop/package.json`: name, description
- `frontend/desktop/src-tauri/tauri.conf.json`: productName, identifier

### Documentation
- All `.md` files in `docs/`
- `README.md`
- All guide files

### Code Files
- Class names: `SelFlowApp` → `CelFlowApp`
- Variable names: `selflow_*` → `celflow_*`
- String literals and comments
- Log messages and print statements
- Environment variable names

### Configuration
- YAML config files
- Environment variable references
- Database table names if any

## Execution Order
1. Stop running system
2. Rename files and directories
3. Update file contents
4. Update package configurations
5. Update documentation
6. Test system functionality
7. Update repository name on GitHub

## Critical Files Priority
1. Launch scripts (system entry points)
2. Package configuration files
3. Main application files
4. Documentation files
5. Configuration files

## Post-Refactor Tasks
1. Update GitHub repository name
2. Update domain references to celflow.com
3. Update any hardcoded paths
4. Verify all imports still work
5. Test complete system functionality 