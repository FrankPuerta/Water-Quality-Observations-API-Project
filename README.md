# Water-Quality-Observations-API-Project

*SETUP*
First:
Open terminal
run "python -m venv .venv"
run ".\.venv\Scripts\Activate"
run "pip install -r requirements.txt"
you also mught wanna throw in "python.exe -m pip install --upgrade pip"

in ./venv make a .env file
in the .env file put in your mongodb info in this format:

MONGO_PASS = your mongodb password
MONGO_USER = mongodb user name
MANGO_CLUSTER_URL = example "cluster0.9uszccd.mongodb.net"

! Make sure to go to your mongoDB Atlas and add your Current IP address to list of allowed to make sure everything runs smoothly.  

If this is your first time running this program make sure to run dbclient.py in order to fill your database with required info

Next step is setting up environment:

To run flask api run "flask --app flaskAPI run"
To run streamlit run "streamlit run client.py"
