# nba-database-project
This is my final project for CS4620 Database Systems, which is a data visualization tool connected to a database of nba player daily statistics. It also displays league leaders, and some team stats.

The main purpose is to see trends of players for the purpose of fantasy and sports betting.

# How to run
Currently using venv which is not included in repository.
Required python libraries are:
- bs4
- pandas
- requests
- streamlit
- sqlite3

Use pip to install the libraries in own venv, which can be created with:
```
python -m venv venv
venv\Scripts\activate # Activates virtual environment (on windows)
```

Then run the following to install all needed libraries:
```
pip install -r requirements.txt
```

To run frontend with streamlit:
```
streamlit run main.py
```
This will also scrape data into database as it includes the various steps of doing so. So it will take a little bit to load if the database hasn't been recently updated.


# Database
The database is currently hosted locally, it is included in database which isn't ideal. Mainly for ease of access. In perfect world it would be hosted elsewhere and more protected

