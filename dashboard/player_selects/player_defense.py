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
        combined_results = pd.DataFrame()
        results = []
        for player in players:
            # Ensure player name is not None or empty
            if player and player.strip():
                player_query = f"""
                SELECT Season, `Name`, `DRS`, `UZR`, `UZR_150`, `Def`, `OAA`
                FROM `raw_data`.`fielding_stats`
                WHERE LOWER(`Name`) LIKE LOWER('%{player}%') AND `Season` >= {season_start} AND `Season` <= {season_end}
                ORDER BY `Season`
                """
                
                result = run_query(player_query)
                if not result.empty:
                    combined_results = pd.concat([combined_results, result])

        if not combined_results.empty:
            # Convert stats to numeric
            numeric_stats = ["DRS", "UZR", "UZR_150", "Def", "OAA"]
            for stat in numeric_stats:
                combined_results[stat] = pd.to_numeric(
                    combined_results[stat], errors="coerce"
                )

            # Aggregate stats
            aggregated_results = combined_results.groupby(
                ["Season", "Name"], as_index=False
            )[numeric_stats].sum()

            color_palette = ["#e3b505", "#db504a", "#4f6d7a", "#56a3a6", "#084c61"]
            unique_names = sorted(aggregated_results["Name"].unique())
            color_mapping = {
                name: color_palette[i % len(color_palette)]
                for i, name in enumerate(unique_names)
            }

            stats = numeric_stats

            st.dataframe(aggregated_results)

            # Display charts in two columns
            for i in range(0, len(stats), 2):
                cols = st.columns(2)  # Create two columns for side-by-side charts
                with cols[0]:
                    if i < len(stats):
                        st.subheader(stats[i])
                        chart = create_altair_chart(
                            aggregated_results, stats[i], color_mapping
                        )
                        st.altair_chart(chart, use_container_width=True)
                if i + 1 < len(stats):
                    with cols[1]:
                        st.subheader(stats[i + 1])
                        chart = create_altair_chart(
                            aggregated_results, stats[i + 1], color_mapping
                        )
                        st.altair_chart(chart, use_container_width=True)
        else:
            st.error("No results found. Please check the input criteria.")
    else:
        st.info("Please submit a query.")


if __name__ == "__main__":
    defense()
