@echo off

setlocal enabledelayedexpansion

set LOGFILE=logs\03_backend_validation.log

if not exist logs mkdir logs

echo ================================================== > "%LOGFILE%"

call :log "Starting backend validation"

if not exist .venv\Scripts\python.exe goto missing_venv

set PYTHON_EXE=.venv\Scripts\python.exe



call :log "Running startup_check.py"

"%PYTHON_EXE%" startup_check.py >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto validation_failed



call :log "Generating backend status snapshot"

"%PYTHON_EXE%" -c "import json; from pathlib import Path; from backend import eterna_core_manager, modules; mgr=eterna_core_manager.EternaCoreManager(); svc=[modules.LlamaService(), modules.ImageService(), modules.TTSService(), modules.WhisperService(), modules.EmotionService(), modules.MemoryManager(), modules.SystemControl(), modules.NetworkManager(), modules.SecurityManager(), modules.SelfUpdateManager(), modules.CommerceManager(), modules.TaskOrchestrator()]; mgr.load_modules(svc); mgr.start(); Path('logs').mkdir(exist_ok=True); Path('logs/backend_status.json').write_text(json.dumps(mgr.status_report(), indent=2), encoding='utf-8'); mgr.stop()" >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto validation_failed



call :log "Backend validation completed successfully"

echo Backend validation finished. Review %LOGFILE% and logs\backend_status.json.

exit /b 0



:missing_venv

call :log "ERROR: Virtual environment not found. Run 01.bat first."

echo Virtual environment missing. Run 01.bat first.

exit /b 1



:validation_failed

call :log "Backend validation failed. Review log for errors."

echo Backend validation encountered errors. See %LOGFILE%.

exit /b 1



:log

echo [%date% %time%] %~1>>"%LOGFILE%"

exit /b 0

