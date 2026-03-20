@echo off
setlocal enabledelayedexpansion
REM ============================================
REM ClawDesk Server Launcher
REM Load environment from .env.dev and start server
REM ============================================
cd /d "%~dp0"

REM Check if .env.dev exists
if not exist ".env.dev" (
    echo ERROR: .env.dev not found! Copy .env.example to .env.dev and fill in your credentials.
    pause
    exit /b 1
)

REM Load env vars from .env.dev (skip comments and empty lines)
for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env.dev") do (
    if not "%%A"=="" if not "%%B"=="" (
        set "%%A=%%B"
    )
)

REM Override: disable Supabase Realtime WebSocket (blocks on Windows)
set SUPABASE_REALTIME_URL=

echo Starting ClawDesk server on http://localhost:%PORT%
echo Press Ctrl+C to stop
python -u -m uvicorn server.main:app --host 0.0.0.0 --port %PORT%
