import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="NBA League Leaders",
    page_icon=":basketball:"
)

st.header("NBA Stat League Leaders")
st.write("*With minimum of 10 games played")

# Getting top 5 individual stat leaders in various categories
# Must have played in at least 10 games
connection = sqlite3.connect('data.db')
top_points = pd.read_sql_query(
    '''SELECT Player, AVG(PTS) AS PPG
       FROM dailyStats
       GROUP BY Player
       HAVING COUNT(Player) >= 10
       ORDER BY PPG DESC
       LIMIT(5)
    ''', connection
)

top_rebounds = pd.read_sql_query(
    '''SELECT Player, AVG(REB) AS RPG
       FROM dailyStats
       GROUP BY Player
       HAVING COUNT(Player) >= 10
       ORDER BY RPG DESC
       LIMIT(5)
    ''', connection
)

top_assists = pd.read_sql_query(
    '''SELECT Player, AVG(AST) AS APG
       FROM dailyStats
       GROUP BY Player
       HAVING COUNT(Player) >= 10
       ORDER BY APG DESC
       LIMIT(5)
    ''', connection
)

top_threes = pd.read_sql_query(
    '''SELECT Player, AVG("3PM") AS "3PG"
       FROM dailyStats
       GROUP BY Player
       HAVING COUNT(Player) >= 10
       ORDER BY "3PG" DESC
       LIMIT(5)
    ''', connection
)

top_steals = pd.read_sql_query(
    '''SELECT Player, AVG(STL) AS SPG
       FROM dailyStats
       GROUP BY Player
       HAVING COUNT(Player) >= 10
       ORDER BY SPG DESC
       LIMIT(5)
    ''', connection
)

top_blocks = pd.read_sql_query(
    '''SELECT Player, AVG(BLK) AS BPG
       FROM dailyStats
       GROUP BY Player
       HAVING COUNT(Player) >= 10
       ORDER BY BPG DESC
       LIMIT(5)
    ''', connection
)

# Getting team stats, points scored, points allowed (against)
# Also retrieving some other stats like assists, and rebounds for teams
team_average_points = pd.read_sql_query('''
    SELECT AVG(TotalPTS) AS AvgPPG, Tm
    FROM (                      
        SELECT SUM(PTS) AS TotalPTS, Tm, Date
        FROM dailyStats
        GROUP BY Date, Tm
        )
    GROUP BY Tm
    ORDER BY AvgPPG DESC                               
    ''', connection
)

team_average_points_against = pd.read_sql_query('''
    SELECT AVG(TotalPTS) AS AvgPPG, Opp
    FROM (                      
        SELECT SUM(PTS) AS TotalPTS, Opp, Date
        FROM dailyStats
        GROUP BY Date, Opp
        )
    GROUP BY Opp
    ORDER BY AvgPPG DESC                               
    ''', connection

)

team_average_assists = pd.read_sql_query('''
    SELECT AVG(TotalAST) AS AvgAST, Tm
    FROM (                      
        SELECT SUM(AST) AS TotalAST, Tm, Date
        FROM dailyStats
        GROUP BY Date, Tm
        )
    GROUP BY Tm
    ORDER BY AvgAST DESC                               
    ''', connection
)

team_average_rebounds = pd.read_sql_query('''
    SELECT AVG(TotalREB) AS AvgREB, Tm
    FROM (                      
        SELECT SUM(REB) AS TotalREB, Tm, Date
        FROM dailyStats
        GROUP BY Date, Tm
        )
    GROUP BY Tm
    ORDER BY AvgREB DESC                               
    ''', connection
)

data = pd.read_sql_query('SELECT * FROM dailyStats', connection)
teams = pd.read_sql_query('SELECT * FROM teams', connection)


# Making stats one hundredths format
top_points = top_points.style.format(precision=2)
top_rebounds = top_rebounds.style.format(precision=2)
top_assists = top_assists.style.format(precision=2)
top_threes = top_threes.style.format(precision=2)
top_steals = top_steals.style.format(precision=2)
top_blocks = top_blocks.style.format(precision=2)
team_average_points_style = team_average_points.style.format(precision=2)
team_average_assists = team_average_assists.style.format(precision=2)
team_average_rebounds = team_average_rebounds.style.format(precision=2)

# Top 5 leaders in main statistical categories
col1, col2 = st.columns([400,400])
with col1:
    # Points
    st.subheader("Top 5 PPG")
    st.dataframe(data=top_points, width=400)
with col2:
    # Rebounds
    st.subheader("Top 5 RPG")
    st.dataframe(data=top_rebounds, width=400)
col3, col4 = st.columns([400,400])
with col3:
    # Assists
    st.subheader("Top 5 APG")
    st.dataframe(data=top_assists, width=400)
with col4:
    # Threes
    st.subheader("Top 5 3PG")
    st.dataframe(data=top_threes, width=400)
col5, col6 = st.columns([400, 400])
with col5:
    # Steals
    st.subheader("Top 5 SPG")
    st.dataframe(data=top_steals, width=400)
with col6:
    # Blocks
    st.subheader("Top 5 BPG")
    st.dataframe(data=top_blocks, width=400)

# Team stat leaders
st.subheader("Stat Leaders by Team")

col7, col8, col9, = st.columns([10,10,10])
with col7:
    st.write("Teams by points")
    st.dataframe(data=team_average_points_style, width=400)
with col8:
    st.write("Teams by assists")
    st.dataframe(data=team_average_assists, width=400)
with col9:
    st.write("Teams by rebounds")
    st.dataframe(data=team_average_rebounds, width=400)

st.subheader("Team points for and against graph")
merged_data = pd.merge(
    team_average_points, team_average_points_against,
    left_on='Tm', right_on='Opp', suffixes=('_for', '_against')
)

# Below is a graph that is based off Kirk Goldsberry's work, where he basically plots team stats with two axis and using averages as axis
# Mine is a simplified version, just wanted to give some credit for the inspiration

# Calculate league averages for both points scored and points scored against
league_avg_for = merged_data['AvgPPG_for'].mean()
league_avg_against = merged_data['AvgPPG_against'].mean()

# Create a scatter plot for points scored by the team vs. points scored against the team
plt.figure(figsize=(8, 8))
plt.scatter(merged_data['AvgPPG_for'], merged_data['AvgPPG_against'], marker='o', c='blue')

# Plot the league averages
plt.axvline(x=league_avg_for, color='red', linestyle='--', label='League Avg for')
plt.axhline(y=league_avg_against, color='green', linestyle='--', label='League Avg against')

# Add team names as points on the plot
for i, team in merged_data.iterrows():
    plt.text(team['AvgPPG_for'], team['AvgPPG_against'], team['Tm'], fontsize=12, ha='center', va='bottom')

plt.xlabel('AvgPPG for')
plt.ylabel('AvgPPG against')
plt.title('AvgPPG for vs. AvgPPG against')
plt.legend()
st.pyplot(plt)   

connection.close()