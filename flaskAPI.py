from flask import Flask, jsonify
import pandas as pd
from dotenv import load_dotenv
import os
from pymongo import MongoClient


# Load .env file from the '.venv' subfolder
load_dotenv(dotenv_path='./.venv/.env')

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MANGO_CLUSTER_URL = os.getenv("MANGO_CLUSTER_URL")

url = (f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MANGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName=Cluster0")
# print(url)

client = MongoClient(url)
db = client["water_quality_data"]


app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "routes":{
            "/api/health": "Health of API",
            "/api/observations": "List of all water quality observations",
            "/api/stats": "Water quality statistics",
            "/api/outliers": "Water quality outlier information",
        }
    })

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/api/observations")
def get_observations():
    return jsonify({"message": "This endpoint will return water quality observations."})

@app.route("/api/stats")
def get_stats():
    return jsonify({"message": "This endpoint will return water quality observations."})

@app.route("/api/outliers")
def get_outliers():
    return jsonify({"message": "This endpoint will return water quality observations."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)        