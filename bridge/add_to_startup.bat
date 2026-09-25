@echo off
REM Is3meo Bridge - start with Windows (v0.4.0)
REM Creates a minimized shortcut to run_bridge.bat in your Startup folder.
cd /d "%~dp0"
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Startup')+'\Is3meo Bridge.lnk'); $s.TargetPath='%~dp0run_bridge.bat'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save()"
echo Is3meo Bridge will start with Windows. Delete "Is3meo Bridge" from shell:startup to undo.
pause
