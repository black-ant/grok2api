@echo off
setlocal

if "%SERVER_HOST%"=="" set SERVER_HOST=0.0.0.0
if "%SERVER_PORT%"=="" set SERVER_PORT=8222
if "%SERVER_WORKERS%"=="" set SERVER_WORKERS=1

set "UV_CMD="
where uv >nul 2>nul
if not errorlevel 1 set "UV_CMD=uv"

set "PYTHON_CMD="
if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=.venv\Scripts\python.exe"
if not defined PYTHON_CMD (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=python"
)
if not defined PYTHON_CMD (
  where py >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=py -3"
)
if not defined PYTHON_CMD (
  echo [ERROR] Python 3.13+ is not installed or not in PATH.
  exit /b 1
)

echo Starting Grok2API on http://%SERVER_HOST%:%SERVER_PORT%

if defined UV_CMD (
  call %UV_CMD% sync
  if errorlevel 1 exit /b 1
  call %UV_CMD% run granian --interface asgi --host %SERVER_HOST% --port %SERVER_PORT% --workers %SERVER_WORKERS% main:app
  exit /b %errorlevel%
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  call %PYTHON_CMD% -m venv .venv
  if errorlevel 1 exit /b 1
)

set "VENV_PY=.venv\Scripts\python.exe"
echo Installing dependencies with pip...
call "%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 exit /b 1
call "%VENV_PY%" -m pip install -e .
if errorlevel 1 exit /b 1

call "%VENV_PY%" -m granian --interface asgi --host %SERVER_HOST% --port %SERVER_PORT% --workers %SERVER_WORKERS% main:app
