from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("cleaned_datasets/2022-nov16.csv")

@app.route('/')
def index():
    return "Water Quality Flask API. route:/data"

@app.route("/data")
def data():
    return jsonify(df.head(5).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)