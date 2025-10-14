from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("cleaned_datasets/2022-nov16.csv")

@app.route("/")
def index():
    return "Welcome to the Water Quality Observations API!"

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("api/observations")
def get_observations():
    return jsonify({"message": "This endpoint will return water quality observations."})

@app.route("/api/observations/<start_date>/<end_date>")
def get_observations_by_date(start_date, end_date):
    return jsonify({"message": "This endpoint will return water quality summary stats for numeric fields."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
