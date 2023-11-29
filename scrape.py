import io
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_all_stats():
    start_date = datetime(year=2023, month=10, day=24)
    end_date = datetime.today() - timedelta(days=1)
    print(end_date)
    
    current_date = start_date
    while current_date <= end_date:
        get_days_stats(current_date)
        current_date = current_date + timedelta(days=1)

def get_days_stats(date):
    day = date.day
    print(day)
    month = date.month
    print(month)
    year = date.year
    print(year)

    filename_date = date.strftime("%m_%d_%Y")
    file_name = f"data\daily_box_scores_{filename_date}.html"
    if not os.path.exists(file_name):
        # Getting data if file doesn't exist
        response = requests.get(f"https://www.basketball-reference.com/friv/dailyleaders.fcgi?month={month}&day={day}&year={year}&type=all")
        with open(file_name, "w+", encoding='utf-8') as f:
            f.write(response.text)
        print(f"File {file_name} created.")
    #else:
        #print(f"File {file_name} already exists.")
    with open(file_name, encoding='utf-8') as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    if soup.find(id="stats"):
        stats_table = soup.find_all(id="stats")
        html_string = str(stats_table)
        html_file = io.StringIO(html_string)

        daily_stats = pd.read_html(html_file)
        daily_stats = daily_stats[0]
        daily_stats = daily_stats.loc[daily_stats['Player'] != 'Player']
        daily_stats = daily_stats.rename(columns={'Unnamed: 3':'Home/Away', 'Unnamed: 5':'Win/Loss'})
        daily_stats['Home/Away'] = daily_stats['Home/Away'].apply(lambda x: 'A' if x == '@' else 'H')

        daily_csv = f'data\daily_stats_{filename_date}.csv'
        if not os.path.exists(daily_csv):
            daily_stats.to_csv(f'data\daily_stats_{filename_date}.csv', index=False)
    else:
        print(f"{filename_date} does not have a stats table")


get_all_stats()
