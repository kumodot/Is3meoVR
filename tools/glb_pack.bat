@echo off
REM GLB Pack v1.0.0 - drag a .glb or .gltf onto this file: one .glb with JPEG textures
REM Marcelo Souza / Kumodot.art - 2026 // @Msouza3d
cd /d "%~dp0"
python glb_pack_v1.0.0.py "%~1"
pause
