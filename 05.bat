@echo off

setlocal enabledelayedexpansion

set LOGFILE=logs\05_packaging.log

if not exist logs mkdir logs

echo ================================================== > "%LOGFILE%"

call :log "Starting packaging and deployment checks"

if not exist .venv\Scripts\python.exe goto missing_venv

set PYTHON_EXE=.venv\Scripts\python.exe



call :log "Running dependency verification script"

"%PYTHON_EXE%" installers\check_dependencies.py >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto packaging_failed



call :log "Collecting backend status summary"

"%PYTHON_EXE%" -c "import json; from pathlib import Path; data=json.loads(Path('logs/backend_status.json').read_text(encoding='utf-8')) if Path('logs/backend_status.json').exists() else {}; Path('logs/backend_status_summary.json').write_text(json.dumps(data, indent=2), encoding='utf-8')" >> "%LOGFILE%" 2>>&1



if not exist dist mkdir dist

if not exist dist\installer mkdir dist\installer



call :log "Checking for Inno Setup compiler (ISCC)"

where iscc >> "%LOGFILE%" 2>>&1

if errorlevel 1 (

    call :log "Inno Setup compiler not found. Skipping installer build."

) else (

    call :log "Building installer via Inno Setup"

    iscc installers\eterna_setup.iss /Odist\installer >> "%LOGFILE%" 2>>&1

    if errorlevel 1 goto packaging_failed

)



call :log "Packaging step completed successfully"

echo Packaging checks complete. Review %LOGFILE% for results.

exit /b 0



:missing_venv

call :log "ERROR: Virtual environment not found. Run 01.bat first."

echo Virtual environment missing. Run 01.bat first.

exit /b 1



:packaging_failed

call :log "Packaging step encountered errors. Review log."

echo Packaging failed. See %LOGFILE%.

exit /b 1



:log

echo [%date% %time%] %~1>>"%LOGFILE%"

exit /b 0

