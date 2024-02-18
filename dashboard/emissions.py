import streamlit as st
import pandas as pd
import altair as alt
from sidebar import sidebar


@st.cache_data
def ghg_emissions():
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    df = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_National_Greenhouse_Gas_Emissions_Invent"
        """
    )

    # Drop the specified columns
    df.drop(
        [
            "ISO2",
            "ISO3",
            "Indicator",
            "Unit",
            "Source",
            "CTS Code",
            "CTS Full Descriptor",
            "Scale",
        ],
        axis=1,
        inplace=True,
    )

    df.drop(
        [
            "1970",
            "1971",
            "1972",
            "1973",
            "1974",
            "1975",
            "1976",
            "1977",
            "1978",
            "1979",
            "1980",
            "1981",
            "1982",
            "1983",
            "1984",
            "1985",
            "1986",
            "1987",
            "1988",
            "1989",
            "1990",
            "1991",
            "1992",
            "1993",
            "1994",
            "1995",
            "1996",
            "1997",
            "1998",
            "1999",
            "2000",
            "2001",
            "2002",
            "2003",
            "2004",
            "2005",
            "2006",
            "2007",
            "2008",
            "2009",
            "2022",
            "2023",
            "2024",
            "2025",
            "2026",
            "2027",
            "2028",
            "2029",
            "2030",
        ],
        axis=1,
        inplace=True,
    )

    # Filter for greenhouse gas emissions
    # Filter by 'Gas Type' and 'CTS_Name'
    df_filtered = df[
        (df["Gas Type"] == "Greenhouse gas")
        & (
            df["CTS Name"]
            == "Total GHG Emissions Including Land-Use and Land-Use Change and Forestry"
        )
    ]
    # st.dataframe(df_filtered)
    # Select columns containing emissions data
    emissions_columns = df_filtered.loc[:, "2010":"2021"]

    # Clean the columns by replacing concatenated strings with empty strings
    emissions_columns_cleaned = emissions_columns.replace(r"[^\d.]", "", regex=True)

    # Convert the cleaned columns to numeric values
    emissions_columns_numeric = emissions_columns_cleaned.apply(
        pd.to_numeric, errors="coerce"
    )

    # Sum the numeric values for each year column across all countries
    total_emissions = emissions_columns_numeric.sum().round(2)

    # Create a new DataFrame with 'Year' and 'Total Emissions' columns
    df_total_emissions = pd.DataFrame(
        {
            "Year": df_filtered.columns[
                4:
            ],  # Assuming columns from 3 to the end are years
            "Total Emissions": total_emissions,
        }
    )

    # Resetting the index to make Year a column
    df_total_emissions.reset_index(drop=True, inplace=True)
    df_total_emissions_cleaned = df_total_emissions.dropna(subset=["Total Emissions"])
    # Create Altair bar chart
    bar_chart = (
        alt.Chart(df_total_emissions)
        .mark_bar(color="#EF626C")
        .encode(
            x=alt.X("Year:N", title="Year"),
            y=alt.Y("Total Emissions:Q", title="Emissions in Millions of Tons"),
            tooltip=["Year:N", "Total Emissions:Q"],
        )
        .properties(height=550)
    )
    df_total_emissions_cleaned = df_total_emissions.dropna(subset=["Total Emissions"])
    # Line chart code provided by user

    line_chart = (
        alt.Chart(df_total_emissions_cleaned)
        .mark_line(color="#3590F3")
        .transform_window(rolling_mean="mean(Total Emissions)", frame=[-9, 0])
        .encode(x="Year:O", y="rolling_mean:Q", tooltip=["Year:O", "rolling_mean:Q"])
    )

    combined_chart = alt.layer(bar_chart, line_chart)

    # Display the chart using streamlit
    st.altair_chart(combined_chart, use_container_width=True)
