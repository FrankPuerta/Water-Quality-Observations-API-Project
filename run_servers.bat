@echo off
echo ============================
echo Starting Flask API and Streamlit Client
echo ============================

:: Activate virtual environment
call .\.venv\Scripts\activate

:: Start Flask API in a new window
start "Flask API" cmd /k "flask --app flaskAPI run"

:: Wait 3 seconds to make sure Flask starts first
timeout /t 3 >nul

:: Start Streamlit client in a new window
start "Streamlit Client" cmd /k "streamlit run client.py"

echo ============================
echo Both servers are running!
echo Flask: http://127.0.0.1:5000
echo Streamlit: http://localhost:8501
echo ============================

pause
