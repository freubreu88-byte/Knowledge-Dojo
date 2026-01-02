@echo off
setlocal

echo [INFO] Starting Vibe-Dojo...

REM Check if .venv exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at .venv\Scripts\python.exe
    echo [INFO] Please run "python -m venv .venv" and install dependencies.
    pause
    exit /b 1
)

REM Activate venv (optional but good context)
call .venv\Scripts\activate.bat

REM Verify youtube-transcript-api version
echo [INFO] Verifying dependencies...
.venv\Scripts\python.exe -c "import youtube_transcript_api; print(f'youtube-transcript-api: {youtube_transcript_api.__version__}')"

REM Run the application
echo [INFO] Launching Interactive CLI...
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, '.'); from vibe_dojo.cli import app; app()"

if %errorlevel% neq 0 (
    echo [ERROR] Dojo crashed with exit code %errorlevel%
    pause
) else (
    echo [INFO] Dojo exited cleanly.
)

pause
