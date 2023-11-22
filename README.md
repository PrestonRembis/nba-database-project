# nba-database-project
This is my final project for CS4620 Database Systems, which is a data visualization tool connected to a database of nba player daily statistics.

The main purpose is to see trends of players for the purpose of fantasy and sports betting.

# How to run
Currently using venv which is not included in repository.
Required python libraries are:
- bs4
- pandas
- requests
- streamlit

Use pip to install the libraries in own venv, which can be created with:
```
python -m venv venv
```

To run scraping program to gather all daily stats until previous day (need data file which will hold all html code (temp function) and csv files):
```
python .\scrape.py
```

To run frontend with streamlit:
```
streamlit run main.py
```


# Database
The database is currently on my personal machine but will eventually be pushed to the repository. Currently importing the csv files into the database using:
```
sqlite3 _.db # Connecting sqlite3 to database
.mode csv
.import daily_stats_month_day_year.csv dailyStats
```
