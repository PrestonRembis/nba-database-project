import os
import pandas as pd

# Where csv files are stored
directory = "data"

# Initial empty data fram
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

# Combine all dataframes into one big one
combined_data = pd.concat(dfs, ignore_index=True)

# Save the combined dataframe to a new file
combined_data.to_csv("allDailyStats.csv", index=False)

# Update message
print('Combining data into csv file...')
