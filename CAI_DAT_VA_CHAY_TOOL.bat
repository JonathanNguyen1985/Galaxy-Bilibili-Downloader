@echo off
title HE THONG TU DONG HOA GALAXY - SETUP & RUN
color 0b

echo ======================================================
echo       DANG KIEM TRA MOI TRUONG CHAY TOOL GALAXY
echo ======================================================
echo.

:: 1. Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0c
    echo [LOI] Khong tim thay Python tren may tinh cua anh!
    echo Vui long tai va cai dat Python tai: https://www.python.org/
    echo Nho tich chon "Add Python to PATH" khi cai dat nhe anh.
    pause
    exit
)

:: 2. Cap nhat pip va cai dat thu vien
echo [+] Dang kiem tra va cai dat thu vien Python...
python -m pip install --upgrade pip >nul
pip install customtkinter yt-dlp

:: 3. Kiem tra file aria2c.exe (De tang toc tai)
if not exist "aria2c.exe" (
    color 0e
    echo [CANH BAO] Khong tim thay file aria2c.exe trong thu muc.
    echo Tool van se chay nhung toc do tai video se bi cham hon.
    echo Anh nen copy file aria2c.exe vao day de dat toc do cao nhat!
    echo.
)

:: 4. Kiem tra file FFmpeg (Bat buoc de ghep video Bilibili)
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    color 0e
    echo [CANH BAO] Khong tim thay FFmpeg tren PATH.
    echo Neu tai video Bilibili ma bi loi khong co tieng, 
    echo anh nho kiem tra lai cai dat FFmpeg nhe!
)

echo.
echo ======================================================
echo       MOI TRUONG DA SAN SANG! DANG MO TOOL...
echo ======================================================
echo.

:: 5. Chay Tool (Dung python de hien CMD hoac pythonw de an CMD)
python bili_downloader.py

pause