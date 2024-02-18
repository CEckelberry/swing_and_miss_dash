import streamlit as st  
from google.oauth2 import service_account
from google.cloud import bigquery  
import pandas as pd

def player_select():
# Create two columns
    # Initialize connection.
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)
    # Perform query.
    def run_query(query):
        query_job = client.query(query, location="us-east4")
        rows_raw = query_job.result()
        # Convert to DataFrame
        df = pd.DataFrame([dict(row) for row in rows_raw])
        # Ensure Season is an integer (should not add commas)
        df['Season'] = df['Season'].astype(str)
        return df
    
    col1, col2, col3, col4 = st.columns(4)

    #Multiple input columns
    with col1:
        player1 = st.text_input("Player 1", key="player1")
    with col2:
        player2 = st.text_input("Player 2", key="player2")
    with col3:
        player3 = st.text_input("Player 3", key="player3")
    with col4:
        player4 = st.text_input("Player 4", key="player4")
