@echo off
REM Light Spill Lab launcher - v0.9.1
REM Starts a local web server in this folder and opens the app in the browser.
REM Quest 3 over USB (developer mode + adb installed):
REM   adb reverse tcp:8080 tcp:8080
REM   then open http://localhost:8080/light_spill_lab_v0.9.1.html in the Quest Browser
cd /d "%~dp0"
set FILE=light_spill_lab_v0.9.1.html

where python >nul 2>nul
if %errorlevel%==0 (
  start "Light Spill Lab server" python -m http.server 8080
  timeout /t 2 >nul
  start "" http://localhost:8080/%FILE%
) else (
  echo Python not found, opening the file directly.
  start "" "%FILE%"
)
