import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Team Stats",
    page_icon=":basketball:"
)

connection = sqlite3.connect('data.db')

# Getting team names, logo file names
teams = pd.read_sql_query('''
    SELECT City, Nickname, Abbreviation, Logo
    FROM teams
    ''', connection
)

# Making new column for full team name, i.e. Ohio Bobcats rather than City: Ohio, Nickname: Bobcats
teams['Full Name'] = teams['City'] + " " + teams['Nickname']
# Dictionary that correlates each team name to their abbreviation
team_mapping = dict(zip(teams['Full Name'], teams['Abbreviation']))

# Using dictionary to get team's abbreviation
def get_team_abbreviation(full_name):
    return team_mapping.get(full_name)

# Option to chose team from list
selected_team = st.sidebar.selectbox("Select a team", teams['Full Name'])

selected_team_abbreviation = get_team_abbreviation(selected_team)
team_logo = selected_team_abbreviation.lower() + ".png"

# Displaying logo and team name side by side
col1, mid, col2 = st.columns([10,1,10])
with col1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.header(selected_team)
with col2:
    st.image(f"images/{team_logo}", width=200)

# Getting player averages for specified team
team_stats = pd.read_sql_query('''
    SELECT Player, AVG(PTS) AS PPG, AVG(REB) AS RPG, AVG(AST) AS APG, AVG(STL) AS SPG, AVG(BLK) AS BPG, AVG("FG%") AS "AvgFG%", AVG("3PM") AS "3PG",  COUNT(*) AS GP
    FROM dailyStats
    WHERE Tm=?
    GROUP BY Player
''', connection, params=[selected_team_abbreviation]
)

# Setting to one hundredths format
team_stats_stylized = team_stats.style.format(precision=2)

st.subheader("Team Player Averages")

st.dataframe(team_stats_stylized, width=800)

# Making a bar chart for player averages on team
if not team_stats.empty:
    st.subheader("Bar Chart for Player Stats")
    # Let user choose which stat to display
    selected_stat = st.selectbox("Select a statistic", ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'AvgFG%', '3PG'])

    plt.figure(figsize=(10, 6))
    plt.bar(team_stats['Player'], team_stats[selected_stat])
    plt.xlabel('Players')
    plt.ylabel(selected_stat)
    plt.title(f'{selected_stat} for Players in {selected_team_abbreviation}')
    plt.xticks(rotation=45, ha='right') # Rotating player names to fit full names on graph
    st.pyplot(plt)
else:
    st.write("No stats found for the selected team.")
