@echo off
cd /d %~dp0
if not exist llama\llama-server.exe (echo Run 00_Setup.bat first. & pause & exit /b 1)
start /min cmd /c "timeout /t 10 /nobreak >nul & start http://127.0.0.1:8080"
llama\llama-server.exe -m models\Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf -ngl 999 --fit on -c 32768 --host 127.0.0.1 --port 8080
pause
