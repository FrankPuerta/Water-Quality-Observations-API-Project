from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd

# Load .env file from the '.venv' subfolder
load_dotenv(dotenv_path='./.venv/.env')

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_CLUSTER_URL = os.getenv("MANGO_CLUSTER_URL")

url = (f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName=Cluster0")
# print(url)

client = MongoClient(url)
# print(client)

db = client["water_quality_data"]
robot1 = db["asv_1"]

print(f"Connected to MongoDB database: {db.name}, collection: {robot1.name}")

# """Example 1"""
# obs1 = {"temperature (C)": 87.2, "salinity (ppt)": 60.2, "odo (mg/L)": 6.7}

# result1=robot1.insert_one(obs1)
# print("Inserted IDs in Example 1", result1.inserted_id)

for filename in os.listdir("cleaned_datasets"):
    if filename.endswith('.csv'):
        file_path = os.path.join("cleaned_datasets", filename)
        print(f'Processing {file_path}...')


        df = pd.read_csv(file_path)

        data_dict = df.to_dict("records")
        if data_dict:
            result = robot1.insert_many(data_dict)
            print(f"Inserted {len(result.inserted_ids)} records from {filename} into MongoDB.")
        else:
            print(f"No data to insert from {filename}.")