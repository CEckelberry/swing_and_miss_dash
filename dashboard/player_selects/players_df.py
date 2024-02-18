import streamlit as st  
from google.oauth2 import service_account
from google.cloud import bigquery  
import pandas as pd

def player_calculator():
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
        # df['Season'] = df['Season'].astype(str)
        return df
    
    #imported state selections
    season_start = st.session_state.get('season_start')
    season_end  = st.session_state.get('season_start')
    player_1  = st.session_state.get('player1')
    player_2  = st.session_state.get('player2')
    player_3  = st.session_state.get('player3')
    player_4  = st.session_state.get('player4')
    players = [player_1, player_2, player_3, player_4]  # Placeholder names

    if st.button('Query'):
      results = []
      for player in players:
          player_query = f"""
              SELECT
                  Season,
                  `Name` AS Name, 
                  `wRC_` AS `wRC+`, 
                  `wOBA` AS wOBA, 
                  `OPS` AS OPS, 
                  `BABIP` AS BABIP, 
                  `AVG` AS `AVG`,
                  `OBP` AS OBP, 
                  `SLG` AS SLG,
                  `WAR` AS WAR, 
                  `K_` AS `K%`, 
                  `BB_` AS `BB%`, 
                  `HR` AS HR, 
                  `Def` AS Def,
                  `SB` AS SB,
                  `CS` AS CS,
                  `BsR` AS BsR,
                  `_3B` AS `3B`,
                  `_2B` AS `2B`,
                  `RBI` AS RBI,
                  `H` AS H,
                  `Age` AS Age,
                  `G` AS G, 
                  `PA` AS PA
              FROM `batting`.`indv_batting_stats`
              WHERE `Name` LIKE '%{player}%'
              AND `Season` >= {season_start} AND `Season` <= {season_end}
              ORDER BY `Season`
          """
          result = run_query(player_query)
          results.append(result)

                # Combine all player results into a single DataFrame
      combined_results = pd.concat(results, ignore_index=True)
      
      advanced_averages = run_query(
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
      
      # Performing an inner join on the 'Season' column
      result = pd.concat([combined_results, advanced_averages], ignore_index=True)
      result = result.fillna("league_avg")
      
      st.dataframe(result)