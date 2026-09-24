@echo off
REM StremioVR Dev Launcher - local test server (launcher v1.0.0)
REM Serves the whole repo on port 8080 and opens the launcher page.
REM Quest 3 over USB: adb reverse tcp:8080 tcp:8080, then open http://localhost:8080/ in the Quest Browser
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
  start "StremioVR server" python -m http.server 8080
  timeout /t 2 >nul
  start "" http://localhost:8080/index.html
) else (
  echo Python not found, opening the launcher file directly.
  start "" "index.html"
)
