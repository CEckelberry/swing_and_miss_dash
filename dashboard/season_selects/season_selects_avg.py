import streamlit as st  
import pandas as pd
from datetime import datetime

def season_selectors():

    col1, col2, col3, col4 = st.columns(4)

    # Use the first column for the first select box
    with col1:
        # Define seasons in descending order
        seasons_avg_start = list(range(2024, 1960, -1))  # Seasons from 2024 to 1990
        # Season selector with the current year as the default
        # Get the current year
        current_year = datetime.now().year
        selected_avg_season_start = st.selectbox("League Average Season Start", seasons_avg_start, key="selected_avg_season_start", index=0)
    with col2:
        print()
    # Use the second column for the second select box
    with col3:
        print()
        # Define seasons in descending order
        seasons_avg_end = list(range(2024, 1960, -1))  # Seasons from 2024 to 1990
        # Season selector with the current year as the default
        # Get the current year
        current_year = datetime.now().year
        selected_avg_season_end = st.selectbox("League Average Season End", seasons_avg_end, key="selected_avg_season_end", index=0)
    with col4:
        print()
