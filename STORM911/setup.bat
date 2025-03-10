@echo off
setlocal enabledelayedexpansion

:: Storm911 Setup Script for Windows

echo Starting Storm911 Setup...
echo.

:: Check Python version
echo Checking Python version...
python --version > nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.8 or higher.
    exit /b 1
)
for /f "tokens=2" %%I in ('python --version') do set PYTHON_VERSION=%%I
echo Found Python %PYTHON_VERSION%

:: Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Recreating...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)
echo Virtual environment created successfully.

:: Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)
echo Virtual environment activated.

:: Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    exit /b 1
)
echo Pip upgraded successfully.

:: Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    exit /b 1
)
echo Dependencies installed successfully.

:: Create required directories
echo.
echo Creating required directories...
if not exist assets mkdir assets
if not exist EXPORTS mkdir EXPORTS
if not exist logs mkdir logs
if not exist data mkdir data
echo Directories created successfully.

:: Create .env file if it doesn't exist
echo.
echo Checking .env file...
if not exist .env (
    echo Creating .env file...
    (
        echo # Storm911 Environment Configuration
        echo.
        echo # Email Settings
        echo STORM911_EMAIL=your_email@example.com
        echo STORM911_EMAIL_PASSWORD=your_email_password
        echo.
        echo # API Settings
        echo READYMODE_API_USER=your_api_username
        echo READYMODE_API_PASS=your_api_password
    ) > .env
    echo .env file created. Please update with your credentials.
) else (
    echo .env file already exists.
)

:: Run setup test
echo.
echo Running setup test...
python test_setup.py
if errorlevel 1 (
    echo Setup test failed. Please check the errors above.
    exit /b 1
)
echo Setup test completed successfully.

echo.
echo Storm911 setup completed successfully!
echo.
echo To start the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the application: python app.py
echo.
echo For more information, please read the README.md file.

endlocal
