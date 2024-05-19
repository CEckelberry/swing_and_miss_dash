import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
from google.oauth2 import service_account
import datetime

# Credentials and client setup
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials)

# Define team colors
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


# Get the current year and define seasons in descending order
current_year = datetime.datetime.now().year
season = current_year

# Function to fetch data based on the selected season
def fetch_data(query):
    return pd.read_gbq(query, credentials=credentials, dialect='standard')

# Define queries for current season's top and bottom pitchers and teams
def top_bottom_query(stat, table, time_frame='season', top=True, limit=5):
    direction = "DESC" if top else "ASC"
    date_filter = f"AND `upload_date` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)" if time_frame == 'week' else ""
    query = f"""
    SELECT 
        Season, `Team` or `Name`, `W`
    FROM 
        `raw_data`.`{team}`
    WHERE 
        `Season` = {season} {date_filter}
    ORDER BY 
        `{stat}` {direction}
    LIMIT {limit}
    """
    return query

# Fetching and displaying data
# Assuming 'K_9' for pitchers and 'wRC+' for teams as example stats
top_pitchers_season = fetch_data(top_bottom_query('K_9', 'pitching_stats'))
bottom_pitchers_week = fetch_data(top_bottom_query('K_9', 'pitching_stats', 'week', False))
top_teams_week = fetch_data(top_bottom_query('wRC+', 'team_batting_stats', 'week'))
bottom_teams_week = fetch_data(top_bottom_query('wRC+', 'team_batting_stats', 'week', False))

# Displaying data
st.write("## Current Season Insights")
st.write("### Top 5 Pitchers of the Season")
st.dataframe(top_pitchers_season)

st.write("### Bottom 5 Pitchers of Last Week")
st.dataframe(bottom_pitchers_week)

st.write("### Top 5 Teams of Last Week")
st.dataframe(top_teams_week)

st.write("### Bottom 5 Teams of Last Week")
st.dataframe(bottom_teams_week)

# Example of markdown for insights
st.markdown("""
Here are some insights:
- **Top Performers**: Look at the players and teams who have excelled.
- **Underperformers**: Analysis on why certain players and teams might be struggling.
""")

# Visualization with Altair
def create_chart(data, title):
    return alt.Chart(data).mark_bar().encode(
        x=alt.X('Team or Name:N', sort='-y'),
        y='Stat:Q',
        color=alt.Color('Team or Name:N', scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values())))
    ).properties(title=title, width=600, height=400)

st.altair_chart(create_chart(top_pitchers_season, "Top Pitchers This Season"))
st.altair_chart(create_chart(bottom_pitchers_week, "Bottom Pitchers Last Week"))
