@echo off
REM Adds "GLB Pack" to the right-click menu: right-click a .glb / .gltf > Send to > GLB Pack
REM Marcelo Souza / Kumodot.art - 2026 // @Msouza3d
cd /d "%~dp0"
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('SendTo')+'\GLB Pack.lnk'); $s.TargetPath='%~dp0glb_pack.bat'; $s.WorkingDirectory='%~dp0'; $s.Save()"
echo Done. Right-click a .glb or .gltf ^> Send to ^> GLB Pack
pause
