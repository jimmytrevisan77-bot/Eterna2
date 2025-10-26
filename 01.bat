@echo off

setlocal enabledelayedexpansion

set LOGFILE=logs\01_setup_environment.log

if not exist logs mkdir logs

echo ================================================== > "%LOGFILE%"

call :log "Starting environment setup"

where python >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto error_missing_python

set PYTHON_EXE=python

if exist .venv\Scripts\python.exe (

    call :log "Detected existing virtual environment"

    set PYTHON_EXE=.venv\Scripts\python.exe

) else (

    call :log "Creating virtual environment in .venv"

    %PYTHON_EXE% -m venv .venv >> "%LOGFILE%" 2>>&1

    if errorlevel 1 goto error_create_venv

    set PYTHON_EXE=.venv\Scripts\python.exe

)

call :log "Upgrading pip, setuptools, and wheel"

"%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto error_upgrade_tools

call :log "Python environment ready: %PYTHON_EXE%"

echo Environment setup completed successfully.

echo Review %LOGFILE% for details.

exit /b 0



:error_missing_python

call :log "ERROR: Python interpreter not found in PATH"

echo Python interpreter missing. See %LOGFILE%.

exit /b 1



:error_create_venv

call :log "ERROR: Failed to create virtual environment"

echo Virtual environment creation failed. See %LOGFILE%.

exit /b 1



:error_upgrade_tools

call :log "ERROR: Failed to upgrade pip/setuptools/wheel"

echo Package manager upgrade failed. See %LOGFILE%.

exit /b 1



:log

echo [%date% %time%] %~1>>"%LOGFILE%"

exit /b 0

