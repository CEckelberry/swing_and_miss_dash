import altair as alt


def create_altair_chart(data, stat, color_palette):
    # Check if 'League Avg' for the stat is 'na', and filter it out if so
    if data.loc[data["Name"] == "League Avg", stat].iloc[0] == "na":
        filtered_data = data[data["Name"] != "League Avg"]
    else:
        filtered_data = data

    chart = (
        alt.Chart(filtered_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Name:N",
                sort=alt.EncodingSortField(field=stat, op="sum", order="descending"),
                title="Player Name",
            ),
            y=alt.Y(f"{stat}:Q", title=stat),
            color=alt.Color(
                "Name:N",
                legend=alt.Legend(title="Players"),
                scale=alt.Scale(
                    domain=filtered_data["Name"].unique(), range=color_palette
                ),
            ),
            tooltip=["Name:N", alt.Tooltip(f"{stat}:Q", title=stat)],
        )
        .properties(width="container", height=600, title=f"Player {stat} Comparison")
    )
    return chart
