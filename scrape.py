import io
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sqlite3

# Looping through from date of most recent entry in database to day previous of present day
def get_all_stats():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Getting most recent date
    cursor.execute("SELECT Date FROM dailyStats ORDER BY Date DESC LIMIT 1")
    most_recent_date = cursor.fetchone()
    # No dates in database
    if(most_recent_date is None):
        start_date = datetime(year=2023, month=10, day=24) # Start of the season
    else:
        start_date =  datetime.strptime(most_recent_date[0], '%m/%d/%Y') 
    end_date = datetime.today() - timedelta(days=1) # Yesterday
    
    recent_date = start_date
    # If date is older than end date than get stats for dates not in database
    while recent_date <= end_date:
        get_days_stats(recent_date)
        recent_date = recent_date + timedelta(days=1)
    print('Scraping stats...')

def get_days_stats(date):
    day = date.day
    month = date.month
    year = date.year

    filename_date = date.strftime("%m_%d_%Y")
    # Storing html code of website which will extracted with pandas into csv file
    file_name = f"data\daily_box_scores_{filename_date}.html"
    if not os.path.exists(file_name):
        # Getting data if file doesn't exist
        response = requests.get(f"https://www.basketball-reference.com/friv/dailyleaders.fcgi?month={month}&day={day}&year={year}&type=all")
        with open(file_name, "w+", encoding='utf-8') as f:
            f.write(response.text)
    with open(file_name, encoding='utf-8') as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    if soup.find(id="stats"):
        stats_table = soup.find_all(id="stats")
        html_string = str(stats_table)
        html_file = io.StringIO(html_string)

        daily_stats = pd.read_html(html_file)
        daily_stats = daily_stats[0]
        # Getting rid of null rows
        daily_stats = daily_stats.loc[daily_stats['Player'] != 'Player']
        # Renaming columns to describe attributes
        daily_stats = daily_stats.rename(columns={'FG':'FGM','3P':'3PM','FT':'FTM','TRB':'REB','TOV':'TO','Unnamed: 3':'Home/Away', 'Unnamed: 5':'Win/Loss'})
        # Translating home and away stats, on website if player is playing an away game it just shows '@' and nothing for home game
        daily_stats['Home/Away'] = daily_stats['Home/Away'].apply(lambda x: 'A' if x == '@' else 'H')

        daily_csv = f'data\daily_stats_{filename_date}.csv'
        if not os.path.exists(daily_csv):
            daily_stats.to_csv(f'data\daily_stats_{filename_date}.csv', index=False)
    else:
        # Day with no NBA stats, Thanksgiving, Voting day, etc.
        print(f"{filename_date} does not have a stats table")


get_all_stats()
