@echo off
setlocal
cd /d "%~dp0"
title Bank Support Agent

rem --- Python check ---
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY where py >nul 2>nul && set "PY=py -3"
if not defined PY goto :nopython

rem --- Packages (sirf pehli baar time lagta hai) ---
%PY% -m pip install -q -r requirements.txt
if errorlevel 1 goto :pipfail

rem --- Gemini key: environment, .env file, ya abhi poochhkar ---
if not "%GEMINI_API_KEY%"=="" goto :run
if exist ".env" goto :run
set /p GEMINI_API_KEY=Apni Gemini API key paste karein:
set /p SAVE=Is computer par agli baar ke liye save karein? [y/N]:
if /i not "%SAVE%"=="y" goto :run
>".env" echo GEMINI_API_KEY=%GEMINI_API_KEY%
echo Key .env file mein save ho gayi.

:run
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:5000"
%PY% bank_web_app.py
echo.
echo Server band ho gaya. Agar error aaya ho to upar dekhein.
pause
exit /b 0

:nopython
echo Python nahi mila. python.org se Python 3.10+ install karein,
echo install karte waqt "Add Python to PATH" tick karein. Phir ye file dobara chalayein.
pause
exit /b 1

:pipfail
echo Packages install nahi ho paaye. Internet check karein.
pause
exit /b 1
