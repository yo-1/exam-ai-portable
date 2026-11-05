@echo off
cd /d %~dp0kit
if not exist ..\python\python.exe (echo Run 00_Setup.bat first. & pause & exit /b 1)
..\python\python.exe scripts\make_deck.py
..\python\python.exe scripts\make_report.py
echo Deck and report are in kit\out
pause
