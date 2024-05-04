import streamlit as st
import pandas as pd
import altair as alt
from google.oauth2 import service_account
from google.cloud import bigquery
from charts.position_player_chart import create_altair_chart
from formatter.format import format_decimal_columns
import datetime

def pitcher_calculator():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    def run_query(query):
        query_job = client.query(query)
        return pd.DataFrame([dict(row) for row in query_job.result()])

    season_start_player = st.session_state.get("season_start")
    season_end_player = st.session_state.get("season_end")
    players = [st.session_state.get(f"player{i}") for i in range(1, 5)]

    if st.button("Query"):
        results = []
        for player in players:
            if player:  # Ensure player name is not None or empty
                # Get the current year
                current_year = datetime.datetime.now().year

                if season_start_player >= current_year or season_end_player >= current_year:
                    # Query for the current year or later
                    player_query = f"""
                    SELECT 
                        Season, `Name`, SIERA, IP, xFIP, `K_9` AS `K|9`, FIP, `GB_` AS `GB%`, `K_` AS `K%`, BABIP, WAR, 
                        `vFA__sc_` AS `vFA_sc`, ERA, `BB_` AS `BB%`, `BB_9` AS `BB|9`, SO, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`,
                        HR_FB AS `HR|FB`, `K_BB` AS `K|BB`, WHIP, BB, Age
                    FROM 
                        `raw_data`.`pitching_stats`
                    WHERE 
                        LOWER(`Name`) LIKE LOWER('%{player}%') AND `Season` >= {season_start_player} AND `Season` <= {season_end_player}
                        AND `upload_date` = (
                            SELECT MAX(`upload_date`)
                            FROM `raw_data`.`pitching_stats`
                            WHERE LOWER(`Name`) LIKE LOWER('%{player}%') AND `Season` >= {season_start_player} AND `Season` <= {season_end_player}
                        )
                    ORDER BY 
                        `Season`
                    """
                    result = run_query(player_query)
                    if not result.empty:
                        results.append(result)
                else:
                    # Query for seasons before the current year
                    player_query = f"""
                    SELECT 
                        Season, `Name`, SIERA, IP, xFIP, `K_9` AS `K|9`, FIP, `GB_` AS `GB%`, `K_` AS `K%`, BABIP, WAR, 
                        `vFA__sc_` AS `vFA_sc`, ERA, `BB_` AS `BB%`, `BB_9` AS `BB|9`, SO, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`,
                        HR_FB AS `HR|FB`, `K_BB` AS `K|BB`, WHIP, BB, Age
                    FROM 
                        `raw_data`.`pitching_stats`
                    WHERE 
                        LOWER(`Name`) LIKE LOWER('%{player}%') AND `Season` >= {season_start_player} AND `Season` <= {season_end_player}
                    ORDER BY 
                        `Season`
                    """
                    result = run_query(player_query)
                    if not result.empty:
                        results.append(result)

        if results:
            combined_results = pd.concat(results, ignore_index=True)
            
            # Convert specified columns to numeric, coercing errors to NaN
            numeric_columns = ["SIERA", "IP", "xFIP", "K|9", "FIP", "GB%", "K%", "BABIP", "WAR", "vFA_sc", "ERA", "BB%", "BB|9", "SO", "SwStr%", "LOB%", "HR|FB", "K|BB", "WHIP", "BB", "Age"]
            for col in numeric_columns:
                combined_results[col] = pd.to_numeric(combined_results[col], errors='coerce')
            
            # Now format the decimal columns
            combined_results = format_decimal_columns(
                combined_results,
                numeric_columns,
            )

            # Visualize
            color_palette = ["#e3b505", "#db504a", "#4f6d7a", "#56a3a6", "#084c61"]
            unique_names = sorted(combined_results["Name"].unique())
            color_mapping = {
                name: color_palette[i % len(color_palette)]
                for i, name in enumerate(unique_names)
            }

            stats = [
                "SIERA", "IP", "xFIP", "K|9", "FIP", "GB%", "K%", "BABIP", "WAR", "vFA_sc", "ERA", "BB%", "BB|9", "SO", "SwStr%", "LOB%", "HR|FB", "K|BB", "WHIP", "BB", "Age"
            ]

            st.dataframe(combined_results)

            # Iterate through the stats in steps of 2 to create two charts per row, if applicable
            for i in range(0, len(stats), 2):
                cols = st.columns(2)  # Create two columns
                with cols[0]:  # First column
                    st.subheader(stats[i])
                    chart = create_altair_chart(combined_results, stats[i], color_mapping)
                    st.altair_chart(chart, use_container_width=True)

                if i + 1 < len(stats):  # Check if there is a next stat to display
                    with cols[1]:  # Second column
                        st.subheader(stats[i + 1])
                        chart = create_altair_chart(combined_results, stats[i + 1], color_mapping)
                        st.altair_chart(chart, use_container_width=True)
        else:
            st.error("No results found. Please check the input criteria.")
    else:
        st.info("Please submit a query.")

if __name__ == "__main__":
    pitcher_calculator()