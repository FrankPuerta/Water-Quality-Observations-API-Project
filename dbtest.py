import os
import pandas as pd


# Testing to see how data looks after being read in from cleaned_datasets
for filename in os.listdir("cleaned_datasets"):
    if filename.endswith('.csv'):
        file_path = os.path.join("cleaned_datasets", filename)
        print(f'Processing {file_path}...')

        df = pd.read_csv(file_path)

        data_dict = df.to_dict("records")


        break

if data_dict:
    print(data_dict)