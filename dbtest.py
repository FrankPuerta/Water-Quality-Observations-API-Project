import os
import pandas as pd
import requests


# Testing to see how data looks after being read in from cleaned_datasets
# for filename in os.listdir("cleaned_datasets"):
#     if filename.endswith('.csv'):
#         file_path = os.path.join("cleaned_datasets", filename)
#         print(f'Processing {file_path}...')

#         df = pd.read_csv(file_path)

#         data_dict = df.to_dict("records")


#         break

# if data_dict:
#     print(data_dict)

# test stuff?

# TEST TO UNDERSTAND PD DATAFRAME FROM API CALL
baseurl = "http://localhost:5000"

q_url = f"/api/observations?start=10/16/2021&end=11/16/2022&temp_min=25.0&temp_max=33.0&sal_min=0.0&sal_max=50.0&odo_min=2.0&odo_max=8.0&limit=100&page=1"
df = requests.get(f"{baseurl}{q_url}").json()

print(pd.DataFrame(df["items"])["Temperature (c)"])