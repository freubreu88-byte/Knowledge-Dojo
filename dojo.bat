@echo off
REM Wrapper script to run dojo CLI
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, '.'); from vibe_dojo.cli import app; app()" %*
