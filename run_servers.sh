#!/bin/bash
echo "============================"
echo "Starting Flask API and Streamlit Client"
echo "============================"

# Activate virtual environment
source .venv/bin/activate

# Start Flask API in background
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && source .venv/bin/activate && flask --app flaskAPI run"'

# Wait 3 seconds
sleep 3

# Start Streamlit client in background
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && source .venv/bin/activate && streamlit run client.py"'

echo "============================"
echo "Both servers are running!"
echo "Flask: http://127.0.0.1:5000"
echo "Streamlit: http://localhost:8501"
echo "============================"
