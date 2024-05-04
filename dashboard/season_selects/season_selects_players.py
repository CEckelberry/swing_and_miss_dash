import streamlit as st  
from datetime import datetime


def season_selectors_player():

    col1, col2, col3, col4 = st.columns(4)

    # Use the first column for the first select box
    with col1:
        # Define seasons in descending order
        seasons = list(range(2024, 1960, -1))  # Seasons from 2024 to 1990
        # Season selector with the current year as the default
        # Get the current year
        current_year = datetime.now().year
        season_start = st.selectbox('Select the start season:', seasons, index=0, key="season_start")
    with col2:
        print()
    # Use the second column for the second select box
    with col3:
        print()
        # Define seasons in descending order
        seasons_2 = list(range(2024, 1960, -1))  # Seasons from 2024 to 1990
        # Season selector with the current year as the default
        # Get the current year
        current_year = datetime.now().year
        season_end = st.selectbox('Select the end season:', seasons_2, index=0, key="season_end")
    with col4:
        print()
