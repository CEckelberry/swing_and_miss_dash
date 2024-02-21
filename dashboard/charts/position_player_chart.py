import altair as alt
import pandas as pd


def create_altair_chart(data, stat, color_mapping):
    filtered_data = (
        data
        if data.loc[data["Name"] == "League Avg", stat].iloc[0] != "na"
        else data[data["Name"] != "League Avg"]
    )

    # Adjust chart y-axis label precision based on stat and apply percentage formatting for K% and BB%
    if stat in ["K%", "BB%"]:
        # Assuming 'data' is your DataFrame and 'stat' is the column name like 'K%' or 'BB%'
        data[stat] = pd.to_numeric(
            data[stat], errors="coerce"
        )  # Convert to numeric, making 'na' into NaN
        data[stat] = data[stat] * 100  # Perform the multiplication by 100
        data[stat] = data[stat].fillna("na")  # Convert NaN back to 'na' strings

        print(data[stat])
        y_axis = alt.Y(
            f"{stat}:Q",
            title=stat,
            axis=alt.Axis(format=".0%"),  # Format as percentage with no decimal places
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
