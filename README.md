# 🌊 Water Quality Observations API Project

## 🚀 Setup Instructions

Follow these steps to set up and run the project successfully.

---

### 🧩 Step 1: Create and Activate a Virtual Environment

Open your terminal and run the following commands:

```
# Create the virtual environment
python -m venv .venv

# Activate it
# On Windows:
.\.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```
Then install all the dependencies:
```
pip install -r requirements.txt
```

Optional but recommended:
```
python.exe -m pip install --upgrade pip
```

### 🗂️ Step 2: Create Configuration Files
Inside your project’s root folder:
1.	Create a .gitignore file with the following content:
```
*
```

2. Create a .env file and add your MongoDB credentials in this format:
```
MONGO_PASS = your_mongodb_password
MONGO_USER = your_mongodb_username
MONGO_CLUSTER_URL = cluster0.9uszccd.mongodb.net
```

## ⚠️ Important:
#### Go to your MongoDB Atlas account and add your current IP address to the list of allowed addresses. Otherwise, your connection may fail.

### 🧠 Step 3: Initialize the Database
If this is your first time running the program, you must populate your database with the required information by running:
```
python dbclient.py
```

### ⚙️ Step 4: Run the Applications
To start the Flask API, run:
```
flask --app flaskAPI run
```
To run the Streamlit client run:
```
streamlit run client.py
```

### Your Flask API and Streamlit frontend should now be running and connected to your MongoDB database.
