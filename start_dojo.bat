@echo off
setlocal
echo [INFO] Starting Vibe-Dojo...

REM Define Python Path
set PYTHON_EXE=.venv\Scripts\python.exe

REM Check Environment
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Virtual environment broken or missing at %PYTHON_EXE%
    echo [INFO] Recreating environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -e ".[dev]"
    pip install --upgrade --force-reinstall youtube-transcript-api>=0.6.0
    pip install google-api-python-client
) else (
    echo [INFO] Venv found. Verifying dependencies...
)

REM Diagnosis
"%PYTHON_EXE%" -c "import sys; print(f'Python: {sys.executable}'); import youtube_transcript_api; print(f'YouTube API Version: {youtube_transcript_api.__version__} at {youtube_transcript_api.__file__}')"

REM Run App
echo [INFO] Launching...
"%PYTHON_EXE%" -c "import sys; sys.path.insert(0, '.'); from vibe_dojo.cli import app; app()"

if %errorlevel% neq 0 (
    echo [ERROR] App crashed with code %errorlevel%
    pause
    exit /b %errorlevel%
)

echo [INFO] Exited cleanly.
pause
