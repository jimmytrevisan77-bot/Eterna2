@echo off

setlocal enabledelayedexpansion

set LOGFILE=logs\04_frontend_build.log

if not exist logs mkdir logs

echo ================================================== > "%LOGFILE%"

call :log "Starting frontend build"

where dotnet >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto missing_dotnet



call :log "Restoring .NET dependencies"

dotnet restore frontend\Eterna.Desktop.csproj >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto build_failed



call :log "Building WPF application (Release)"

dotnet build frontend\Eterna.Desktop.csproj -c Release >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto build_failed



call :log "Publishing standalone build to dist\frontend"

dotnet publish frontend\Eterna.Desktop.csproj -c Release -o dist\frontend --self-contained false >> "%LOGFILE%" 2>>&1

if errorlevel 1 goto build_failed



call :log "Frontend build completed successfully"

echo Frontend build finished. Output available in dist\frontend.

exit /b 0



:missing_dotnet

call :log "ERROR: dotnet CLI not found in PATH"

echo .NET SDK not found. Install .NET 8 SDK and retry. See %LOGFILE%.

exit /b 1



:build_failed

call :log "Frontend build failed. Review log for compiler output."

echo Frontend build failed. Check %LOGFILE%.

exit /b 1



:log

echo [%date% %time%] %~1>>"%LOGFILE%"

exit /b 0

