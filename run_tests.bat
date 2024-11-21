@echo off

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Start the HTTP server in the background
start python -m http.server 8000
set SERVER_PID=%ERRORLEVEL%

:: Give the server a moment to start
timeout /t 3 /nobreak > nul

:: Run pytest
pytest tests\selenium_script.py

:: Kill the server after tests are done
taskkill /PID %SERVER_PID% /F > nul 2>&1

:: Deactivate virtual environment
deactivate
