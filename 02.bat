@echo off
setlocal enabledelayedexpansion
set LOGFILE=logs\02_install_dependencies.log
if not exist logs mkdir logs
echo ================================================== > "%LOGFILE%"
call :log "Starting dependency installation"
if not exist .venv\Scripts\python.exe goto missing_venv
set PYTHON_EXE=.venv\Scripts\python.exe
set FAILED=0

call :pip_install "Core tooling" "%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 set FAILED=1

call :pip_install "PyTorch CUDA 12.4 stack" "%PYTHON_EXE%" -m pip install torch==2.2.2+cu124 torchvision==0.17.2+cu124 torchaudio==2.2.2+cu124 --index-url https://download.pytorch.org/whl/cu124
if errorlevel 1 set FAILED=1

call :pip_install "Core AI services" "%PYTHON_EXE%" -m pip install chromadb tinydb langchain faiss-cpu==1.7.4
if errorlevel 1 set FAILED=1

call :pip_install "Emotion intelligence" "%PYTHON_EXE%" -m pip install speechbrain deepface hsemotion==0.2.0 librosa
if errorlevel 1 set FAILED=1

call :pip_install "System control" "%PYTHON_EXE%" -m pip install pyautogui psutil openrgb-python keyboard mouse
if errorlevel 1 set FAILED=1

call :pip_install "Self update and security" "%PYTHON_EXE%" -m pip install gitpython guardrails-ai cryptography pyotp watchdog
if errorlevel 1 set FAILED=1

call :pip_install "Vision enhancement" "%PYTHON_EXE%" -m pip install realesrgan rembg opencv-python pillow
if errorlevel 1 set FAILED=1

call :pip_install "Commerce integrations" "%PYTHON_EXE%" -m pip install shopifyapi requests beautifulsoup4 selenium
if errorlevel 1 set FAILED=1

call :pip_install "Autonomy orchestration" "%PYTHON_EXE%" -m pip install apscheduler langgraph python-socketio[client] aiohttp
if errorlevel 1 set FAILED=1

call :log "Installing Printify API helper from GitHub"
"%PYTHON_EXE%" -m pip install git+https://github.com/ralphbean/printify-api.git >> "%LOGFILE%" 2>>&1
if errorlevel 1 (
    call :log "ERROR: Printify API helper installation failed"
    set FAILED=1
) else (
    call :log "Printify API helper installed"
)

call :pip_install "Final validation" "%PYTHON_EXE%" -m pip check
if errorlevel 1 set FAILED=1

if %FAILED%==1 goto dependency_failure
call :log "Dependency installation completed successfully"
echo Dependencies installed. Review %LOGFILE% for details.
exit /b 0

:missing_venv
call :log "ERROR: Virtual environment not found. Run 01.bat first."
echo Virtual environment missing. Run 01.bat first.
exit /b 1

:dependency_failure
call :log "One or more dependency installations failed. Review log."
echo Dependency installation encountered errors. See %LOGFILE%.
exit /b 1

:pip_install
set STEP=%~1
shift
set CMD=%*
call :log "Installing %STEP% using: %CMD%"
%CMD% >> "%LOGFILE%" 2>>&1
if errorlevel 1 (
    call :log "ERROR installing %STEP%"
    exit /b 1
)
call :log "Completed %STEP%"
exit /b 0

:log
echo [%date% %time%] %~1>>"%LOGFILE%"
exit /b 0
