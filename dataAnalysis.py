import numpy as np
import pandas as pd
import os

input_folder = 'datasets'
output_folder = 'cleaned_datasets'

os.makedirs(output_folder, exist_ok=True)

columns = [
        # "Conductivity (mmhos/cm)", Needed to take this one out because its all 0's causing an error
        "Temperature (c)", 
        "Salinity (ppt)", 
        "Temp C", 
        "Sal ppt", 
        "pH", 
        "pH mV", 
        "Turbid+ NTU", 
        "Chl ug/L",
        "BGA-PC cells/mL",
        "ODOsat %",
        "ODO mg/L"
        ]

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        print(f'Processing {file_path}...')
        
        df = pd.read_csv(file_path)
        
        means = df[columns].mean(axis=0)
        stds = df[columns].std(axis=0, ddof=0)
        
        z_scores = (df[columns] - means) / stds

        
        mask  = (np.abs(z_scores) <= 3).all(axis=1)
        cleaned_df = df[mask]
        
        total_rows = len(df)
        cleaned_rows = total_rows - len(cleaned_df)
        remaining_rows = len(cleaned_df)
        
        print(f"Total rows originally: {total_rows}")
        print(f"Rows removed as outliers: {cleaned_rows}")
        print(f"Rows remaining after cleaning: {remaining_rows}")
        
        
        output_path = os.path.join(output_folder, filename)
        cleaned_df.to_csv(output_path, index=False)
        
        print(f"  ✅ Saved to: {output_path}")
        
print("\nAll datasets processed successfully!\n\n")