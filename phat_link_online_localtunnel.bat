@echo off
title Phat Web App E-Logistics Len Internet (Live Public Link)
cd /d "%~dp0"

echo ================================================================
echo  🏭 DICH VU PHAT WEB APP DEMO LEN INTERNET DE CHIA SE
echo ================================================================
echo Dang lay dia chi IP public (mat khau mo link localtunnel neu can)...
curl -s https://loca.lt/mytunnelpassword
echo.
echo ----------------------------------------------------------------
echo Dang khoi dong Web App tren cong 8501 va tao Link Public...
echo (Luu y: Giu nguyen cua so nay mo trong suot buoi thuyet trinh)
echo ----------------------------------------------------------------

set "PY_EXE=C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe"
if exist "%PY_EXE%" (
    start "" /b "%PY_EXE%" -m streamlit run app.py --server.port 8501 --server.headless true
) else (
    start "" /b python -m streamlit run app.py --server.port 8501 --server.headless true
)

timeout /t 3 /nobreak >nul
cmd /c "npx --yes localtunnel --port 8501"

pause
