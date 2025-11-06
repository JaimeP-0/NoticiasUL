@echo off
echo Iniciando servidor Flask...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python app.py
pause

