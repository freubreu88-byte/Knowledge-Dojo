@echo off
call .venv\Scripts\activate.bat
call .venv\Scripts\python.exe -c "import sys; sys.path.insert(0, '.'); from vibe_dojo.cli import app; app()"
pause
