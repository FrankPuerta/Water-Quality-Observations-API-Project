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

observations_url = f"/api/observations?start=10/16/2021&end=11/16/2022&temp_min=25.0&temp_max=33.0&sal_min=0.0&sal_max=50.0&odo_min=2.0&odo_max=8.0&limit=100&page=1"
observations_dataSet = requests.get(f"{baseurl}{observations_url}").json()

# print(observations_dataSet.keys())         # expect: dict_keys(['count','items'])
# print(observations_dataSet.get("count"))   # see how many matched
# print(len(observations_dataSet.get("items", [])))


observations_df = pd.DataFrame(observations_dataSet["items"])

print(f"DataFrame head: \n{observations_df.head()}")

# # print(pd.DataFrame(df["items"])["Temperature (c)"])
# date = "10/16/2021"

# linechart_url = f"http://localhost:5000/api/lineChart?date={date}"
# linechart_dataSet = requests.get(linechart_url).json()

# print(f"Filtered Data for Date: {date}")
# # print(linechart_dataSet)
# linechart_df = pd.DataFrame(linechart_dataSet["data"])
# print(len(linechart_df))
# print(linechart_df[["Time", "Temperature (c)", "Salinity (ppt)", "ODO mg/L"]])

# subset = linechart_df.iloc[0:10]
# print("\nSubset of Line Chart Data (First 10 Rows):")
# print(subset)

# print(filtered_df[["Time", "Temperature (c)", "Salinity (ppt)", "ODO mg/L"]])