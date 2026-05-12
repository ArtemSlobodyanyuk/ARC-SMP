@echo off
setlocal

REM Prefer project venv if present (no console: pythonw).
set "VENV_PYW=%~dp0..\..\.venv\Scripts\pythonw.exe"
if exist "%VENV_PYW%" (
  "%VENV_PYW%" -m arc %*
  exit /b %ERRORLEVEL%
)

REM Fallback to system pythonw on PATH.
pythonw -m arc %*
exit /b %ERRORLEVEL%

