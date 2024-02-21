import streamlit as st
import pandas as pd
import altair as alt
from google.oauth2 import service_account
from google.cloud import bigquery
from charts.position_player_chart import create_altair_chart
from formatter.format import format_decimal_columns


def player_calculator():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    def run_query(query):
        query_job = client.query(query)
        return pd.DataFrame([dict(row) for row in query_job.result()])

    season_start = st.session_state.get("season_start")
    season_end = st.session_state.get("season_end")
    season_start_player = st.session_state.get("season_start_player")
    season_end_player = st.session_state.get("season_end_player")
    players = [st.session_state.get(f"player{i}") for i in range(1, 5)]

    if st.button("Query"):
        results = []
        for player in players:
            if player:  # Ensure player name is not None or empty
                player_query = f"""
                SELECT Season, `Name`, AVG, OBP, SLG, `wRC_` AS `wRC+`, wOBA, OPS, BABIP, WAR, `K_` AS `K%`, `BB_` AS `BB%`, HR, Def, SB, CS, BsR, `_3B` AS `Triples`, `_2B` AS `Doubles`, RBI, `H` AS Hits, Age, G, PA
                FROM `batting`.`indv_batting_stats`
                WHERE LOWER(`Name`) LIKE LOWER('%{player}%') AND `Season` >= {season_start_player} AND `Season` <= {season_end_player}
                ORDER BY `Season`
                """
                result = run_query(player_query)
                if not result.empty:
                    results.append(result)

        if results:
            combined_results = pd.concat(results, ignore_index=True)
            combined_results = format_decimal_columns(
                combined_results,
                ["AVG", "OBP", "SLG", "wOBA", "OPS", "BABIP"],
            )

            # Handle League Avg
            league_avg_query = f"""
            SELECT Season, 'League Avg' AS Name, AVG, OBP, SLG, `wRC_` AS `wRC+`, wOBA, OPS, BABIP, NULL AS WAR, NULL AS `K%`, NULL AS `BB%`, NULL AS HR, NULL AS Def, NULL AS SB, NULL AS CS, NULL AS BsR, NULL AS `Triples`, NULL AS `Doubles`, NULL AS RBI, NULL AS Hits, NULL AS Age, NULL AS G, NULL AS PA
            FROM `league_avg_batting`.`advanced`
            WHERE `Season` >= {season_start} AND `Season` <= {season_end}
            ORDER BY `Season`
            """
            advanced_averages = run_query(league_avg_query)
            result = pd.concat(
                [combined_results, advanced_averages], ignore_index=True
            ).fillna("na")

            # Visualize
            color_palette = ["#e3b505", "#db504a", "#4f6d7a", "#56a3a6", "#084c61"]
            unique_names = sorted(result["Name"].unique())
            color_mapping = {
                name: color_palette[i % len(color_palette)]
                for i, name in enumerate(unique_names)
            }

            stats = [
                "AVG",
                "OBP",
                "SLG",
                "HR",
                "wRC+",
                "SB",
                "CS",
                "BsR",
                "Triples",
                "Doubles",
                "RBI",
                "Hits",
                "wOBA",
                "WAR",
                "K%",
                "BB%",
                "OPS",
                "BABIP",
            ]

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
    player_calculator()
