import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
from google.oauth2 import service_account
import datetime

# Credentials and client setup
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials)

# Define team colors and seasons
team_colors = {
    "Braves": "#13274f",
    "Guardians": "#e31937",  # Current name
    "Indians": "#e31937",   # Former name
    "Cardinals": "#c41e3a",
    "Royals": "#bd9b60",
    "Nationals": "#ab0003",
    "Twins": "#002b5c",
    "Padres": "#2f241d",
    "Diamondbacks": "#a71930",
    "Angels": "#ba0021",
    "White Sox": "#27251f",
    "Astros": "#eb6e1f",
    "Blue Jays": "#134a8e",
    "Brewers": "#0a2351",
    "Orioles": "#df4601",
    "Giants": "#fd5a1e",
    "Phillies": "#e81828",
    "Cubs": "#0e3386",
    "Pirates": "#fdb827",
    "Tigers": "#0c2340",
    "Rangers": "#003278",
    "Mets": "#ff5910",
    "Rays": "#8fbce6",
    "Mariners": "#005c5c",
    "Red Sox": "#bd3039",
    "Rockies": "#33006f",
    "Dodgers": "#005a9c",
    "Yankees": "#0c2340",
    "Reds": "#c6011f",
    "Marlins": "#00a3e0",
    "Athletics": "#003831"
}

# Define seasons in descending order
seasons = list(range(2024, 1960, -1))  # Seasons from 2024 to 1990

# Season selector with the current year as the default
# Get the current year
current_year = datetime.datetime.now().year
season = st.selectbox('Select the season:', seasons, index=0)

# Fetch data based on the selected season
def fetch_data(season):
    if season >= current_year:
    # Query for seasons 2024 or later, filtering by the latest 'upload_date'
        query = f"""
        SELECT 
            Season, `Team`, DPS, UZR, UZR_150, Def, OAA, ErrR
        FROM 
            `raw_data`.`team_fielding_stats`
        WHERE 
            `Season` = {season}
            AND `upload_date` = (
                SELECT MAX(`upload_date`)
                FROM `raw_data`.`team_fielding_stats`
                WHERE `Season` = {season}
            )
        """
    else:
        # Query for seasons before 2024, ignoring 'upload_date'
        query = f"""
        SELECT 
            Season, `Team`, DPS, UZR, UZR_150, Def, OAA, ErrR
        FROM 
            `raw_data`.`team_fielding_stats`
        WHERE 
            `Season` = {season}
        """
    return pd.read_gbq(query, credentials=credentials, dialect='standard')

data = fetch_data(season)
print(data)

# Display charts for each stat, sorted by the statistic value
stat_columns = data.columns[2:]  # Exclude 'Season' and 'Team' columns for stats
for stat in stat_columns:
    print(f"Generating chart for: {stat}")  # Debug which stat is being processed
    # Sort the data frame by the current stat in descending order before charting
    sorted_data = data.sort_values(by=stat, ascending=False)
    print(sorted_data[[stat, 'Team']].head()) # Show top sorted data for the current stat
    chart = alt.Chart(sorted_data).mark_bar().encode(
        x=alt.X('Team:N', title='Team', sort=alt.SortField(field=stat, order='descending')),  # Apply sorting to the x-axis based on y values
        y=alt.Y(stat, title=stat.replace('_', ' ')),
        color=alt.Color('Team:N', scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values()))),
        tooltip=['Team', stat]
    ).properties(
        width=1300,
        height=750,
        title=f'Team {stat} for {season}'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)