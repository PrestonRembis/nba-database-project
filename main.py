import streamlit as st
import numpy as np
import pandas as pd

daily_stats = pd.read_csv("daily_stats_11_18_2023")

st.subheader('Daily Stats')
st.write(daily_stats)
st.bar_chart(daily_stats, x='Player',  y='PTS')
