@echo off
cd /d %~dp0kit
if not exist ..\python\python.exe (echo Run 00_Setup.bat first. & pause & exit /b 1)
..\python\python.exe scripts\make_charts.py
..\python\python.exe scripts\make_maps.py
..\python\python.exe scripts\make_dem.py
echo Figures regenerated in kit\assets
pause
