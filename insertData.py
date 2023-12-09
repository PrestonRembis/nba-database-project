import io
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import requests
import scrape
import combine
import sqlite3

# Checking to see if specified date is in database
def date_exists_in_db(date):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Date FROM dailyStats ORDER BY Date DESC LIMIT 1")
    most_recent_date = cursor.fetchone()
    
    conn.close()

    if most_recent_date is None:
        return False
    elif date > most_recent_date[0]:
        return False
    else:
        return True

# Inserting date's dataframe into database
def insert_into_db(dataframe):
    conn = sqlite3.connect('data.db')

    # Replace empty values with 0
    dataframe = dataframe.fillna(0)

    # Adding dataframe to database
    dataframe.to_sql('dailyStats', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

# Getting all dates already in database
def get_dates_from_csv(csv):
    df = pd.read_csv(csv)
    dates = df['Date'].unique()
    return dates

# Looking for any new data and inserting it into database
def insert_new_data(csv):
    conn = sqlite3.connect('data.db')

    unique_dates = get_dates_from_csv(csv)
    # Looping through all dates in database
    for date in unique_dates: 
        if (not date_exists_in_db(date)):
            df_for_date = pd.read_csv(csv)
            df_for_date = df_for_date[df_for_date['Date'] == date]
            insert_into_db(df_for_date)
    conn.close()

    # Update message
    print('Inserting data into database...')

insert_new_data('allDailyStats.csv')