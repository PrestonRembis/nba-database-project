import os
import pandas as pd

# Directory where your daily CSV files are stored
directory = "data"

# Initialize an empty list to store all dataframes
dfs = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        # Read each CSV file and remove 'Rk' column
        df = pd.read_csv(file_path)
        df.drop(columns='Rk', inplace=True)

        # Extract date from the filename and format it
        year = filename.split('_')[-1].replace('.csv', '')  # Extract date and remove extension
        month = filename.split('_')[-3]
        day = filename.split('_')[-2]
        date = f'{month}/{day}/{year}'
        df['Date'] = date  # Update 'Date' column
        dfs.append(df)

# Concatenate all dataframes into a single dataframe
combined_data = pd.concat(dfs, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_data.to_csv("allDailyStats.csv", index=False)
