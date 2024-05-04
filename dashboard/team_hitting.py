import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
from google.oauth2 import service_account

# Credentials and client setup
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials)

# Define team colors and seasons
team_colors = {
    "ARI": "#a71930", "ATL": "#13274f", "BAL": "#df4601", "BOS": "#bd3039",
    "CHC": "#0e3386", "CHW": "#27251f", "CIN": "#c6011f", "CLE": "#e31937",
    "COL": "#33006f", "DET": "#0c2340", "HOU": "#eb6e1f", "KCR": "#bd9b60",
    "LAA": "#ba0021", "LAD": "#005a9c", "MIA": "#00a3e0", "MIL": "#0a2351",
    "MIN": "#002b5c", "NYM": "#ff5910", "NYY": "#0c2340", "OAK": "#003831",
    "PHI": "#e81828", "PIT": "#fdb827", "SDP": "#2f241d", "SEA": "#005c5c",
    "SFG": "#fd5a1e", "STL": "#c41e3a", "TBR": "#8fbce6", "TEX": "#003278",
    "TOR": "#134a8e", "WSN": "#ab0003"
}

# Define seasons in descending order
seasons = list(range(2024, 1960, -1))  # Seasons from 2024 to 1990

# Season selector with the current year as the default
current_year = 2024
season = st.selectbox('Select the season:', seasons, index=0)

# Fetch data based on the selected season
def fetch_data(season):
    query = f"""
    SELECT Season, `Team`, AVG, OBP, SLG, `wRC_` AS `wRC+`, wOBA, OPS, BABIP, WAR, `K_` AS `K%`, `BB_` AS `BB%`, HR, Def, SB, CS, BsR, `3B` AS `Triples`, `2B` AS `Doubles`, RBI, `H` AS Hits, Age
    FROM `raw_data`.`team_batting_stats`
    WHERE `Season` = {season}
    """
    return pd.read_gbq(query, credentials=credentials, dialect='standard')

data = fetch_data(season)

# Display charts for each stat, sorted by the statistic value
stat_columns = data.columns[2:]  # Exclude 'Season' and 'Team' columns for stats
for stat in stat_columns:
    # Sort the data frame by the current stat in descending order before charting
    sorted_data = data.sort_values(by=stat, ascending=False)
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