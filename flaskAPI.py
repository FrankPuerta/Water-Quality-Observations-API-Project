from flask import Flask, jsonify, request
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
robot1 = db["asv_1"]


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

@app.route("/api/stats") #f"{baseurl}/api/stats?field={stat}"
def get_stats():

    field = request.args.get("field", default="ph", type=str)
    count = robot1.count_documents({})
    
    pipeline = [
        {"$group": {
            "_id": None,
            "count": {"$sum": 1},
            "mean":  {"$avg": f"${field}"},
            "min":   {"$min": f"${field}"},
            "max":   {"$max": f"${field}"},
            # MongoDB 5.2+: percentiles
            "pct":   {"$percentile": {
                "p": [0.25, 0.5, 0.75],
                "input": f"${field}",
                "method": "approximate"
            }}
        }},
        {"$project": {
        "_id": 0,
        "field": {"$literal": field},
        "count": 1,
        "mean": {"$round": ["$mean", 3]},
        "min": 1,
        "max": 1,
        "p25": {"$arrayElemAt": ["$pct", 0]},
        "p50": {"$arrayElemAt": ["$pct", 1]},
        "p75": {"$arrayElemAt": ["$pct", 2]}
    }}
    ]

    doc = next(robot1.aggregate(pipeline), None) or {}

    return jsonify({"field": field, **doc})

@app.route("/api/outliers")
def get_outliers():
    return jsonify({"message": "This endpoint will return water quality observations."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)