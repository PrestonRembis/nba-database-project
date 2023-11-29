import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load database into pandas data frame
connection = sqlite3.connect('data.db')
data = pd.read_sql_query('SELECT * FROM dailyStats', connection)
teams = pd.read_sql_query('SELECT * FROM teams', connection)

# Get unique players and stats
players = data['Player'].unique()
stats = data.columns[6:-1]

# Sidebar widgets for user input
selected_player = st.sidebar.selectbox('Select a player', players)
player_team = pd.read_sql_query(f"SELECT Abbreviation FROM teams, dailyStats WHERE Player='{selected_player}' AND Tm=Abbreviation LIMIT(1)",connection)
player_team_logo = player_team.loc[0].to_string()
player_team_logo = player_team_logo.replace("Abbreviation    ","").lower() + '.png'
selected_stat = st.sidebar.selectbox('Select a stat', stats)

# Filter data based on the selected player
player_data = data[data['Player'] == selected_player]
num_past_games = st.sidebar.slider('Select number of past games', min_value=1, max_value=len(player_data))

# Filter data based on user selection with the number of games selected by user
filtered_data = player_data.tail(num_past_games)

# Visualization
st.subheader(f'{selected_player} - {selected_stat} for Last {num_past_games} Games')
fig, ax = plt.subplots(figsize=(8, 6))

# Plotting the selected stat for the chosen player
ax.plot(filtered_data['Date'], filtered_data[selected_stat], marker='o', linestyle='-')
ax.set_xlabel('Date')
ax.set_ylabel(selected_stat)
ax.set_title(f'{selected_player} - {selected_stat}')

# Horizontal line feature
horizontal_line = st.sidebar.number_input('Enter a value for horizontal line', value=0.0)
ax.axhline(y=horizontal_line, color='r', linestyle='--')
above_line = filtered_data[selected_stat] > horizontal_line
times_above_line = above_line.sum()

col1, mid, col2 = st.columns([1,1,10])
with col1:
    st.image(f"images/{player_team_logo}", width=100)
with col2:
    st.write(f"{selected_player} was above {horizontal_line} {times_above_line} times in the last {num_past_games} games.")


# Show the plot in Streamlit
st.pyplot(fig)
