from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from pymongo import MongoClient

from dbclient import MONGO_CLUSTER_URL

# Load .env file from the '.venv' subfolder
load_dotenv(dotenv_path='./.venv/.env')

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_CLUSTER_URLNGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")

url = (f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER_URLNGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName=Cluster0")
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

    args = request.args
    query = {}
    errors = []

    # Date range
    start = args.get("start")
    end = args.get("end")

    # Numeric filters (Temperature, Salinity, ODO)
    def f(name):
        v = args.get(name)
        if v is None or v == "":
            return None
        try:
            return float(v)
        except ValueError:
            errors.append(f"'{name}' must be numeric.")
            return None

    for key, field in {
        ("temp_min", "temp_max"): "Temperature (c)",
        ("sal_min", "sal_max"): "Salinity (ppt)",
        ("odo_min", "odo_max"): "ODO mg/L"
    }.items():
        lo, hi = f(key[0]), f(key[1])
        if lo is not None or hi is not None:
            rng = {}
            if lo is not None:
                rng["$gte"] = lo
            if hi is not None:
                rng["$lte"] = hi
            query[field] = rng

    # Pagination
    try:
        limit = min(max(int(args.get("limit", 100)), 1), 1000)
        skip = max(int(args.get("skip", 0)), 0)
    except ValueError:
        errors.append("Invalid skip or limit.")

    if errors:
        return jsonify({"errors": errors}), 400

    # Run query
    total = robot1.count_documents(query)
    cursor = (
        robot1.find(
            query,
            {
                "_id": 0,
                "Date": 1,
                "Time": 1,
                "Temperature (c)": 1,
                "Salinity (ppt)": 1,
                "ODO mg/L": 1,
            },
        )
        .sort("Time", -1)
        .skip(skip)
        .limit(limit)
    )

    return jsonify({
        "count": total,
        "items": list(cursor)
    })


@app.route("/api/stats") #f"{baseurl}/api/stats?field={stat}"
def get_stats():

    fields = request.args.getlist("field") or ["Temperature (c)", "Salinity (ppt)", "pH"]
    pipes = {}

    for field in fields:
        pipes[field] = [
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

    pipeline = [{"$facet": pipes}]
    result = list(robot1.aggregate(pipeline))
    raw = result[0] if result else {}

    stats = {}
    for field in fields:
        stats[field] = raw.get(field, {})[0]

    return jsonify(stats)

@app.route("/api/outliers")
def get_outliers():
    return jsonify({"message": "This endpoint will return water quality observations."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)