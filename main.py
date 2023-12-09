import insertData
import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Setting configuration of streamlit page
st.set_page_config(
    page_title="NBA Player Stats Visualization",
    page_icon=':basketball:',
)


# Load database into pandas data frame
connection = sqlite3.connect('data.db')
data = pd.read_sql_query('SELECT * FROM dailyStats', connection)
teams = pd.read_sql_query('SELECT * FROM teams', connection)
data['Pts+Reb+Ast'] = data['PTS'] + data['REB'] + data['AST']
data['Pts+Reb'] = data['PTS'] + data['REB']
data['Pts+Ast'] = data['PTS'] + data['AST']
data['Ast+Reb'] = data['AST'] + data['REB']


# Get unique players and stats
players = data['Player'].unique()
stats = data.columns[6:] # Getting columns index 6 and on
stats = stats.drop(['Date'])

# Sidebar widgets for user input
selected_player = st.sidebar.selectbox('Select a player', players)
player_team = pd.read_sql_query(f"SELECT Abbreviation FROM teams, dailyStats WHERE Player=? AND Tm=Abbreviation LIMIT(1)",connection, params=[selected_player])
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
fig, ax = plt.subplots(figsize=(12, 8))

# Plotting the selected stat for the chosen player
ax.plot(filtered_data['Date'], filtered_data[selected_stat], marker='o', linestyle='-')
ax.set_xlabel('Date')
ax.set_ylabel(selected_stat)
ax.set_title(f'{selected_player} - {selected_stat}')
fig.autofmt_xdate() # Does rotation of dates automatically (Really useful!)

# Horizontal line feature for basically seeing over/under trends
horizontal_line = st.sidebar.number_input('Enter a value for horizontal line', value=0.0)
ax.axhline(y=horizontal_line, color='r', linestyle='--')
below_line = filtered_data[selected_stat] < horizontal_line
above_line = filtered_data[selected_stat] > horizontal_line
times_above_line = above_line.sum()
times_below_line = below_line.sum()

# Displaying logo of current player
col1, mid, col2 = st.columns([1,1,10])
with col1:
    st.image(f"images/{player_team_logo}", width=100)
with col2:
    st.write(f"{selected_player} was ABOVE {horizontal_line} {selected_stat} {times_above_line} time(s) in the last {num_past_games} game(s).")
    st.write(f"{selected_player} was BELOW {horizontal_line} {selected_stat} {times_below_line} time(s) in the last {num_past_games} game(s).")



# Show the plot in Streamlit
st.pyplot(fig)

connection.close()
