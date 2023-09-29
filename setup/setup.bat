@echo off
:: Batch script to install Python packages with pip as administrator

:: Check for administrator privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If not administrator, relaunch as administrator
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\admin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/k ""%~0""", "", "runas", 1 >> "%temp%\admin.vbs"
    "%temp%\admin.vbs"
    exit /b
)

:: Install required Python packages
echo Installing sentence-splitter...
pip install sentence-splitter

echo Installing transformers...
pip install transformers

echo Installing SentencePiece...
pip install SentencePiece

echo All packages installed successfully.

:: Remove the temporary VBS script
del "%temp%\admin.vbs"

:: Pause to keep the command prompt window open
pause
