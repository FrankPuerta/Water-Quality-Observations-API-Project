from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime

# Load .env file from the '.venv' subfolder
load_dotenv(dotenv_path='./.venv/.env')

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")

url = (f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName=Cluster0")
print(url)

client = MongoClient(url)

# print(client.list_database_names())

db = client["water_quality_data"]
robot1 = db["asv_1"]


app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "routes":{
            "/api/health": "Health of API",
            "/api/observations?start=<start_date>&end=<end_date>&temp_min=<temp_min>&temp_max=<temp_max>&sal_min=<sal_min>&sal_max=<sal_max>&odo_min=<odo_min>&odo_max=<odo_max>&limit=<limit>&page=<page>": "Filtered water quality observations based on query parameters",
            "/api/lineChart": "Data for line chart visualization",
            "/api/stats": "Water quality statistics",
            "/api/outliers": "Water quality outlier information",
        }
    })

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

def _norm_date_to_db(s) -> str | None:
    s = str(s)
    """Accept 'MM/DD/YY' or 'MM/DD/YYYY' and return 'MM/DD/YY' to match DB."""
    if not s:
        return None
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%m/%d/%y")  # <-- matches your Mongo 'Date' field
        except ValueError:
            continue
    return None

@app.route("/api/observations")
def get_observations():
    args = request.args
    errors = []
    conditions = []

    # ----- Dates -----
    start_in = _norm_date_to_db(args.get("start"))
    end_in   = _norm_date_to_db(args.get("end"))

    allowed_dates = ["10/16/21", "12/16/21", "10/07/22", "11/16/22"]

    if args.get("start") and not start_in:
        errors.append("Invalid 'start' date. Use MM/DD/YY or MM/DD/YYYY.")
    if args.get("end") and not end_in:
        errors.append("Invalid 'end' date. Use MM/DD/YY or MM/DD/YYYY.")

    if not errors and (start_in or end_in):
        if start_in and start_in not in allowed_dates:
            errors.append(f"'start' must be one of {allowed_dates}.")
        if end_in and end_in not in allowed_dates:
            errors.append(f"'end' must be one of {allowed_dates}.")
        if not errors:
            if start_in and end_in:
                i0, i1 = allowed_dates.index(start_in), allowed_dates.index(end_in)
                if i0 > i1:
                    errors.append("'start' must not be after 'end'.")
                else:
                    chosen_dates = allowed_dates[i0:i1+1]
            else:
                chosen_dates = [start_in or end_in]
            if not errors:
                conditions.append({"Date": {"$in": chosen_dates}})

    # ----- Numeric filters -----
    def num(name):
        v = args.get(name)
        if v is None or v == "":
            return None
        try:
            return float(v)
        except ValueError:
            errors.append(f"'{name}' must be numeric.")
            return None

    temp_min, temp_max = num("temp_min"), num("temp_max")
    sal_min,  sal_max  = num("sal_min"),  num("sal_max")
    odo_min,  odo_max  = num("odo_min"),  num("odo_max")
    pH_min, pH_max = num("pH_min"), num("pH_max")

    if temp_min is not None or temp_max is not None:
        rng = {}
        if temp_min is not None: rng["$gte"] = temp_min
        if temp_max is not None: rng["$lte"] = temp_max
        conditions.append({"Temperature (c)": rng})

    if sal_min is not None or sal_max is not None:
        rng = {}
        if sal_min is not None: rng["$gte"] = sal_min
        if sal_max is not None: rng["$lte"] = sal_max
        conditions.append({"Salinity (ppt)": rng})

    if odo_min is not None or odo_max is not None:
        rng = {}
        if odo_min is not None: rng["$gte"] = odo_min
        if odo_max is not None: rng["$lte"] = odo_max
        conditions.append({"ODO mg/L": rng})

    # if pH_min is not None or pH_max is not None:
    #     rng = {}
    #     if pH_min is not None: rng["$gte"] = pH_min
    #     if pH_max is not None: rng["$lte"] = pH_max
    #     conditions.append({"pH": rng})

    if errors:
        return jsonify({"errors": errors}), 400

    query = {"$and": conditions} if conditions else {}

    # ----- Pagination (page -> skip) -----
    try:
        limit = min(max(int(args.get("limit", 100)), 1), 1000)
        page = max(int(args.get("page", 1)), 1)
        skip = (page - 1) * limit
    except ValueError:
        return jsonify({"errors": ["Invalid 'limit' or 'page'."]}), 400

    projection = {
        "_id": 0,
        # "Date": 1,
        "TimeStamp": 1,
        "Temperature (c)": 1,
        "pH": 1,
        "Salinity (ppt)": 1,
        "ODO mg/L": 1,
    }

    total = robot1.count_documents(query)
    cursor = (
        robot1.find(query, projection)
        .sort([("Date", 1), ("Time", 1)])
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

@app.route("/api/lineChart")
def get_line_chart_data():
    arg = request.args
    field = arg.get("date")

    if field not in ["10/16/2021", "12/16/2021", "10/07/2022", "11/16/2022"]:
        return jsonify({"error": "Invalid field. Must be one of: '10/16/2021', '12/16/2021', '10/07/2022', '11/16/2022'."}), 400

    cursor = robot1.find(
        {},
        {
            "_id": 0,
            "Salinity (ppt)": 1,
            "Temperature (c)": 1,
            "ODO mg/L": 1,
            "pH": 1,
            "Date": 1,
            "Time": 1,
            field: 1
        },
    ).sort("Time", 1)

    data = list(cursor)

    if not data:
        return jsonify({"error": "No data found for the specified field."}), 404
    
    return jsonify({
        "field": field,
        "data": data
    })

    

@app.route("/api/outliers")
def get_outliers():
    return jsonify({"message": "This endpoint will return water quality observations."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)