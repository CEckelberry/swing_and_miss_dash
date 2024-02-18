import streamlit as st
import pandas as pd
from pandasql import sqldf
import altair as alt


@st.cache_data
def solar_production():
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    df = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_iea_data"
        """
    )

    solar_filter = sqldf(
        """
        SELECT * 
        FROM df
        WHERE "Product"='Solar'
        """
    )

    solar_filter["Time"] = pd.to_datetime(solar_filter["Time"], format="%B %Y")

    iea_data_benelux_solar_filter = sqldf(
        """
        SELECT Country, strftime('%Y-%m-%d', Time) as DateTime, Product, SUM(Value) as Value
        FROM solar_filter
        WHERE "Country" IN ('Netherlands', 'Belgium', 'Luxembourg')
        GROUP BY DateTime, Country, Product
    """
    )

    monthly_sum = (
        iea_data_benelux_solar_filter.groupby(["DateTime"])["Value"]
        .sum()
        .round(2)
        .reset_index()
    )

    # Altair Chart
    chart = (
        alt.Chart(monthly_sum)
        .mark_bar(color="#3590F3")
        .encode(
            x=alt.X("DateTime:T", title="Month"),
            y=alt.Y("Value:Q", title="GwH Per Month Benelux"),
            color=alt.Color(scale=alt.Scale(scheme="category20"), title="Month"),
        )
        .properties(height=550)
    )

    # Display the chart using streamlit
    st.altair_chart(chart, use_container_width=True)
