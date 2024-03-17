import altair as alt
import pandas as pd


def create_altair_chart(data, stat, color_mapping):
    # First, check if the stat column exists in the dataframe
    if stat not in data.columns:
        print(f"Column '{stat}' not found in the dataframe.")
        return None  # Ensure to handle this case appropriately in your code

    # Initialize filtered_data
    filtered_data = data

    # Check if "League Avg" is in the dataframe and if the stat value for "League Avg" is not "na"
    if "League Avg" in data["Name"].values:
        league_avg_stat_value = data.loc[data["Name"] == "League Avg", stat].iloc[0]
        if league_avg_stat_value == "na":
            # If the league average stat value is "na", exclude "League Avg" from the dataset
            filtered_data = data[data["Name"] != "League Avg"]
    else:
        # If "League Avg" is not present, no additional filtering is needed based on "League Avg"
        # This line could be omitted, as filtered_data is already initialized to data
        filtered_data = data

    # Adjust chart y-axis label precision based on stat and apply percentage formatting for K% and BB%
    if stat in ["K%", "BB%"]:
        # Directly use values as they are without converting to numeric or multiplying by 100
        filtered_data[stat] = filtered_data[stat].str.rstrip('%').astype(float)
        # print(data[stat])
        y_axis = alt.Y(
            f"{stat}:Q",
            title=stat,
            axis=alt.Axis(format=".2f"),  # Format as percentage with no decimal places
        )
    elif stat in ["AVG", "OBP", "SLG", "wOBA", "OPS", "BABIP"]:
        y_axis = alt.Y(f"{stat}:Q", title=stat, axis=alt.Axis(format=".3f"))
    elif stat in [
        "Triples",
        "Doubles",
        "HR",
        "RBI",
        "SB",
        "CS",
        "SO",
        "HBP",
        "wRC+",
        "WAR",
        "Hits",
    ]:
        y_axis = alt.Y(f"{stat}:Q", title=stat)  # No specific format needed
    else:
        y_axis = alt.Y(f"{stat}:Q", title=stat, axis=alt.Axis(format=".2f"))

    chart = (
        alt.Chart(filtered_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Name:N",
                sort=alt.EncodingSortField(field=stat, op="sum", order="descending"),
                title="Player Name",
            ),
            y=y_axis,
            color=alt.Color(
                "Name:N",
                legend=alt.Legend(title="Players"),
                scale=alt.Scale(
                    domain=list(color_mapping.keys()),
                    range=[color_mapping[name] for name in color_mapping.keys()],
                ),
            ),
            tooltip=[
                alt.Tooltip("Name:N", title="Player Name"),
                alt.Tooltip(f"{stat}:Q", title=stat),
            ],
        )
        .properties(width="container", height=600)
    )

    return chart
