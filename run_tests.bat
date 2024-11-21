@echo off

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Start the HTTP server in the background
start /b python -m http.server 8000
set SERVER_PID=%!ERRORLEVEL!

:: Give the server a moment to start
timeout /t 3 /nobreak > nul

:: Run pytest
pytest tests\selenium_script.py

:: Kill the server after tests are done
for /f "tokens=2 delims=," %%a in ('tasklist /fi "imagename eq python.exe" /nh') do (
    taskkill /PID %%a /F > nul 2>&1
)

:: Deactivate virtual environment
call .venv\Scripts\deactivate.bat || echo "Deactivation not necessary in Windows"
