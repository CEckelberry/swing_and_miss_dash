import altair as alt
import streamlit as st
from pandasql import sqldf
import pandas as pd
from datetime import datetime
import altair as alt
from st_pages import Page, show_pages, add_page_title
from sidebar import sidebar
import numpy as np

add_page_title("Energy Production", layout="wide")
sidebar()


@st.cache_data
def energy_production():
    st.subheader("Growth of Solar in the Energy Mix of Benelux")
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    energy_production_benelux = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_energy_production_benelux"
        """
    )

    energy_production_benelux["Value"] = energy_production_benelux["Value"].astype(
        float
    )

    # Filter for the last five years without 2023
    current_year = datetime.now().year
    last_five_years = list(range(current_year - 10, current_year))
    benelux = energy_production_benelux[
        energy_production_benelux["Country"].isin(
            ["Belgium", "Netherlands", "Luxembourg"]
        )
    ]
    benelux = benelux[
        benelux["Time"].apply(lambda x: pd.to_datetime(x).year).isin(last_five_years)
    ]

    # Create t1 DataFrame
    t1 = benelux[benelux["Product"] == "Solar"]
    t1 = (
        t1.groupby(["Country", t1["Time"].apply(lambda x: pd.to_datetime(x).year)])
        .agg({"Value": "sum"})
        .rename(columns={"Value": "GWh Solar"})
        .reset_index()
    )

    # Create t2 DataFrame
    t2 = benelux[
        (benelux["Product"] != "Total Renewables (Hydro, Geo, Solar, Wind, Other)")
        & (benelux["Product"] != "Total Combustible Fuels")
    ]
    t2 = (
        t2.groupby(["Country", t2["Time"].apply(lambda x: pd.to_datetime(x).year)])
        .agg({"Value": "sum"})
        .rename(columns={"Value": "GWh Total"})
        .reset_index()
    )

    # Merge t1 and t2 DataFrames
    merged_df = pd.merge(t1, t2, on=["Country", "Time"])

    # Calculate Solar Share (%)
    merged_df["Solar Share (%)"] = round(
        (merged_df["GWh Solar"] / merged_df["GWh Total"]) * 100, 2
    )

    # Rename the 'Time' column to 'Year'
    merged_df.rename(columns={"Time": "Year"}, inplace=True)

    # Select necessary columns
    result_df = merged_df[
        ["Country", "Year", "GWh Solar", "GWh Total", "Solar Share (%)"]
    ]

    result_df["Year"] = result_df["Year"].apply(lambda x: str(x))
    result_df["Year"] = pd.to_datetime(result_df["Year"])

    # Define color scheme
    colors = ["#17BEBB", "#3590F3", "#EF626C", "#DFC2F2"]

    # Assuming result_df is your original DataFrame
    new_df = result_df[["Year", "Country", "Solar Share (%)"]].copy()

    # Rename the columns in the new DataFrame
    new_df.columns = ["x", "category", "y"]

    source = new_df

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(
        nearest=True, on="mouseover", fields=["x"], empty=False
    )

    # The basic line
    line = (
        alt.Chart(source)
        .mark_line(interpolate="basis")
        .encode(
            x=alt.X("x:T").axis(format="%Y", tickCount="year", title="Year"),
            y=alt.Y("y:Q").axis(title="Solar Share (%)"),
            color=alt.Color("category:N", scale=alt.Scale(range=colors)),
        )
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart(source)
        .mark_point()
        .encode(
            x="x:T",
            y="y:Q",
            opacity=alt.value(0),
        )
        .add_params(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(nearest, "y:Q", alt.value(" "))
    )

    # Draw a rule at the location of the selection
    rules = (
        alt.Chart(source)
        .mark_rule(color="gray")
        .encode(
            x="x:T",
        )
        .transform_filter(nearest)
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(line, selectors, points, rules, text).properties(
        width=600, height=550
    )

    st.altair_chart(chart, use_container_width=True)

    with st.expander("See Data"):
        st.dataframe(result_df)


energy_production()
