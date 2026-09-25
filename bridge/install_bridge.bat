@echo off
REM Is3meo Bridge installer - v0.4.0
REM Installs Playwright for Python. The Bridge uses Microsoft Edge (or Chrome).
cd /d "%~dp0"
python -m pip install --upgrade playwright
if not exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
  echo Google Chrome not found, installing Playwright Chromium as a fallback...
  python -m playwright install chromium
)
echo.
echo Done. Now run run_bridge.bat
pause
