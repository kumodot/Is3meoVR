@echo off
REM SilVRCine Bridge - start with Windows (v0.11.0)
REM Creates a minimized shortcut to run_bridge.bat in your Startup folder (replaces the old "Is3meo Bridge" one).
cd /d "%~dp0"
powershell -NoProfile -Command "$d=[Environment]::GetFolderPath('Startup'); Remove-Item -ErrorAction SilentlyContinue ($d+'\Is3meo Bridge.lnk'); $s=(New-Object -ComObject WScript.Shell).CreateShortcut($d+'\SilVRCine Bridge.lnk'); $s.TargetPath='%~dp0run_bridge.bat'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save()"
echo SilVRCine Bridge will start with Windows. Delete "SilVRCine Bridge" from shell:startup to undo.
pause
