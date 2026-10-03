@echo off
REM Seat Kit Splitter v1.0.0 - drag the Painter GLB (seat + armrest) onto this file
REM Marcelo Souza / Kumodot.art - 2026 // @Msouza3d
cd /d "%~dp0"
python split_seat_kit_v1.0.0.py "%~1"
pause
