@echo off
chcp 65001 >nul
title GitHub Auto Deploy - E-Logistics Dashboard (Nhiem vu 5)

set "GH_EXE=C:\Program Files\GitHub CLI\gh.exe"
set "GIT_EXE="
for /f "tokens=*" %%i in ('where git 2^>nul') do set GIT_EXE=%%i
set "PY_EXE=C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe"
set "PROJECT_DIR=%~dp0"
set "REPO_NAME=elogistics-workforce-planner"

echo ================================================================
echo   GITHUB AUTO DEPLOY - E-LOGISTICS AI WORKFORCE PLANNER
echo   Nhiem vu 5 | Tu dong tao Repo va Upload len GitHub
echo ================================================================
echo.

:: Buoc 1: Dang nhap GitHub (mo trinh duyet tu dong)
echo [Buoc 1/5] Dang nhap tai khoan GitHub cua ban...
echo Mot cua so trinh duyet se tu dong mo ra.
echo Ban hay bam "Authorize GitHub CLI" tren trinh duyet do la xong!
echo.
"%GH_EXE%" auth login --web --git-protocol https
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Dang nhap that bai. Vui long thu lai.
    pause
    exit /b 1
)
echo.
echo [OK] Dang nhap GitHub thanh cong!
echo.

:: Buoc 2: Kiem tra / cai Git
echo [Buoc 2/5] Kiem tra Git...
if "%GIT_EXE%"=="" (
    echo Chua co Git. Dang cai dat tu dong...
    winget install Git.Git --accept-source-agreements --accept-package-agreements --silent
    for /f "tokens=*" %%i in ('where git 2^>nul') do set GIT_EXE=%%i
)
echo [OK] Git san sang: %GIT_EXE%
echo.

:: Buoc 3: Khoi tao Git repo tai thu muc hien tai
echo [Buoc 3/5] Khoi tao Git repository...
cd /d "%PROJECT_DIR%"

if not exist ".git" (
    git init
    git checkout -b main
)

:: Tao file .gitignore
echo __pycache__/ > .gitignore
echo *.pyc >> .gitignore
echo .streamlit/secrets.toml >> .gitignore

git add .
git commit -m "feat: E-Logistics AI Workforce Planner - Nhiem vu 5 (Streamlit Dashboard)" 2>nul || (
    git config user.email "user@elogistics.demo"
    git config user.name "E-Logistics Team"
    git add .
    git commit -m "feat: E-Logistics AI Workforce Planner - Nhiem vu 5 (Streamlit Dashboard)"
)
echo [OK] Da commit code len Git local!
echo.

:: Buoc 4: Tao GitHub Repo moi va push len
echo [Buoc 4/5] Tao GitHub repository va dang tai code...
"%GH_EXE%" repo create %REPO_NAME% --public --source=. --remote=origin --push --description "E-Logistics AI Workforce Planner - Phan bo Nhan su & Bai toan Kinh te Flash Sale (Nhiem vu 5)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Repo co the da ton tai, dang push len...
    git remote set-url origin "https://github.com/%USERNAME%/%REPO_NAME%.git" 2>nul
    git push -u origin main --force
)
echo [OK] Da dang tai code len GitHub!
echo.

:: Buoc 5: Hien thi link ket qua
echo [Buoc 5/5] Lay thong tin repository...
echo.
"%GH_EXE%" repo view --web
echo.
for /f "tokens=*" %%i in ('"%GH_EXE%" repo view --json url -q ".url" 2^>nul') do (
    echo ================================================================
    echo   LINK GITHUB REPOSITORY CUA BAN:
    echo   %%i
    echo.
    echo   LINK DEPLOY LEN STREAMLIT CLOUD (mien phi):
    echo   https://share.streamlit.io
    echo   (Dang nhap = GitHub, chon repo: %REPO_NAME%, file: app.py)
    echo ================================================================
)
echo.
echo Hoan thanh! Nhan phim bat ky de dong cua so nay.
pause
