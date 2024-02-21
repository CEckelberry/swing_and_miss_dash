import streamlit as st
import pandas as pd
import altair as alt
from google.oauth2 import service_account
from google.cloud import bigquery
from charts.position_player_chart import create_altair_chart
from formatter.format import format_decimal_columns


def defense():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    def run_query(query):
        query_job = client.query(query)
        return pd.DataFrame([dict(row) for row in query_job.result()])

    season_start = st.session_state.get("season_start")
    season_end = st.session_state.get("season_end")
    players = [st.session_state.get(f"player{i}") for i in range(1, 5)]

    if st.button("Query Field"):
        results = []
        for player in players:
            if player:  # Ensure player name is not None or empty
                player_query = f"""
                SELECT Season, `Name`, "DRS", "UZR", "UZR_150", "Def", "OAA"
                FROM `fielding`.`indv_fielding_stats`
                WHERE LOWER(`Name`) LIKE LOWER('%{player}%') AND `Season` >= {season_start} AND `Season` <= {season_end}
                ORDER BY `Season`
                """
                result = run_query(player_query)
                if not result.empty:
                    results.append(result)

            # Visualize
            color_palette = ["#e3b505", "#db504a", "#4f6d7a", "#56a3a6", "#084c61"]
            unique_names = sorted(result["Name"].unique())
            color_mapping = {
                name: color_palette[i % len(color_palette)]
                for i, name in enumerate(unique_names)
            }

            stats = ["DRS", "UZR", "UZR_150", "Def", "OAA"]

            st.dataframe(result)

            # Iterate through the stats in steps of 2 to create two charts per row
            for i in range(0, len(stats), 2):
                cols = st.columns(2)  # Create two columns
                with cols[0]:  # First column
                    st.subheader(stats[i])
                    chart = create_altair_chart(result, stats[i], color_mapping)
                    st.altair_chart(chart, use_container_width=True)

                if i + 1 < len(stats):  # Check if there is a next stat to display
                    with cols[1]:  # Second column
                        st.subheader(stats[i + 1])
                        chart = create_altair_chart(result, stats[i + 1], color_mapping)
                        st.altair_chart(chart, use_container_width=True)
        else:
            st.error("No results found. Please check the input criteria.")
    else:
        st.info("Please submit a query.")


if __name__ == "__main__":
    defense()
