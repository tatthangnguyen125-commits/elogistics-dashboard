@echo off
title E-Logistics AI Workforce Planner - Nhiem vu 5
cd /d "%~dp0"

echo ========================================================
echo  E-LOGISTICS AI WORKFORCE PLANNER - NHIEM VU 5
echo ========================================================
echo Dang khoi dong Web App tren Localhost...
echo.

set "PY_EXE=C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe"
if exist "%PY_EXE%" (
    "%PY_EXE%" -m streamlit run app.py --server.port 8501
) else (
    python -m streamlit run app.py --server.port 8501
)

pause
