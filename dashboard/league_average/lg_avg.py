import streamlit as st  
from google.oauth2 import service_account
from google.cloud import bigquery  
import pandas as pd

def avg_calculator():
# Create two columns
    # Initialize connection.
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    def run_query(query):
        query_job = client.query(query, location="us-east4")
        rows_raw = query_job.result()
        # Convert to DataFrame
        df = pd.DataFrame([dict(row) for row in rows_raw])
        # Ensure Season is an integer (should not add commas)
        df['Season'] = df['Season'].astype(str)
        return df
    season_start = st.session_state.get('season_start')
    season_end  = st.session_state.get('season_start')
    avg = run_query(
        f"""select     
              `Season` AS Season,
              `wRC_` AS `wRC+`, 
              `wOBA` AS wOBA, 
              `OPS` AS OPS, 
              `BABIP` AS BABIP, 
              `OBP` AS OBP, 
              `K_` AS `K%`, 
              `BB_` AS `BB%`, 
              `AVG` AS `AVG`,
              `SLG` AS SLG,
              `PA` AS PA 
            FROM `league_avg_batting`.`advanced`
            WHERE `Season` >= { season_start } AND `Season` <= { season_end }
            ORDER BY `Season`""")
    st.dataframe(avg)