import streamlit as st  
from google.oauth2 import service_account
from google.cloud import bigquery  
import pandas as pd
from datetime import datetime, timedelta


def season_selectors_player():
# Create two columns
    # Initialize connection.
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    def seconds_until_end_of_year():
        now = datetime.now()
        next_year = datetime(year=now.year + 1, month=1, day=1)
        delta = next_year - now
        return delta.total_seconds()
    
    # Perform query.
    @st.cache_data(ttl=seconds_until_end_of_year())
    def run_query(query):
        query_job = client.query(query, location="us-east4")
        rows_raw = query_job.result()
        # Convert to DataFrame
        df = pd.DataFrame([dict(row) for row in rows_raw])
        # Ensure Season is an integer (should not add commas)
        #df['Season'] = df['Season'].astype(str)
        return df
    
    seasons = run_query(
        """SELECT DISTINCT `Season`
            FROM swingandmiss.batting.team_batting_stats
            WHERE `Season` >= 1960
            ORDER BY `Season` DESC""")
    col1, col2, col3, col4 = st.columns(4)

    # Use the first column for the first select box
    with col1:
        selected_season_start = st.selectbox("Player Season Start", options=seasons, key="season_start_player")
    with col2:
        print()
    # Use the second column for the second select box
    with col3:
        print()
        selected_season_end = st.selectbox("Player Season End", options=seasons, key="season_end_player")
    with col4:
        print()
