@echo off
REM Get the full path to the batch file's directory
SET "SCRIPT_DIR=%~dp0"

REM Check if Python is installed and accessible
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH. Please install Python first.
    pause
    exit /b
)

REM Check if the script is in the same directory as this batch file
IF NOT EXIST "%SCRIPT_DIR%Program.py" (
    echo The script "Program.py" is missing. Please place it in the same directory as this batch file.
    pause
    exit /b
)

REM Run the Python script using the full path
python "%SCRIPT_DIR%Program.py"

REM Pause to keep the window open after execution
pause
