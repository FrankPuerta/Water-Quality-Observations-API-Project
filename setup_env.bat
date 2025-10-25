@echo off
echo ============================
echo Setting up virtual environment
echo ============================

:: Create virtual environment
python -m venv .venv

:: Activate the environment
call .\.venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

echo ============================
echo Setup complete!
echo To activate your environment again later, run:
echo .\.venv\Scripts\activate
echo ============================

pause
