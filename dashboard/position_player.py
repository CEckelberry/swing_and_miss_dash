import altair as alt
import streamlit as st
from pandasql import sqldf
import pandas as pd
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from google.oauth2 import service_account
from google.cloud import bigquery

add_page_title("Compare Yearly Emissions Sources", layout="wide")

sidebar()


def emissions_sources():
    # Initialize connection.
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)
    # Perform query.
    def run_query(query):
        query_job = client.query(query)
        rows_raw = query_job.result()
        return rows_raw 
    
    emissions = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_CO2_Emissions_Emissions_Intensities_and_"
        """
    )

    emissions = sqldf(
        """
        SELECT "Country", "Industry", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"
        FROM emissions
        """
    )

    # Select relevant columns (including years)
    selected_columns = ["Country", "Industry"] + [
        str(year) for year in range(1995, 2019)
    ]
    emissions_selected = emissions[selected_columns]

    # Melt the DataFrame to reshape it for easier processing
    emissions_melted = pd.melt(
        emissions_selected,
        id_vars=["Country", "Industry"],
        var_name="Year",
        value_name="Emissions",
    )

    # Convert the "Emissions" column to numeric
    emissions_melted["Emissions"] = pd.to_numeric(
        emissions_melted["Emissions"], errors="coerce"
    )

    # Filter for Netherlands, Belgium, Luxembourg, and sum emissions by Industry and Year
    netherlands_belgium_luxembourg = emissions_melted[
        emissions_melted["Country"].isin(["Netherlands", "Belgium", "Luxembourg"])
    ]
    industry_emissions = (
        netherlands_belgium_luxembourg.groupby(["Year", "Industry"])["Emissions"]
        .sum()
        .round(2)
        .reset_index()
    )

    # Get top 10 industries for each year
    top_10_industries = (
        industry_emissions.groupby("Year")
        .apply(lambda x: x.nlargest(10, "Emissions"))
        .reset_index(drop=True)
    )

    years = top_10_industries["Year"].unique().tolist()

    option = st.selectbox(
        "Please Pick a Year",
        (years),
        index=10,
        placeholder="Select Year",
        key="option1",
    )

    filtered_data = top_10_industries[top_10_industries["Year"] == str(option)]

    colors = [
        "#17BEBB",
        "#3590F3",
        "#EF626C",
        "#DFC2F2",
        "#D8D8F6",
        "#c1d7c6",
        "#a3bcf9",
        "#7796cb",
        "#576490",
        "#f6e8ea",
    ]
    # Create Altair chart
    base = (
        alt.Chart(filtered_data)
        .encode(
            alt.Theta("Emissions:Q").stack(True),
            alt.Radius("Emissions:Q").scale(type="sqrt", zero=True, rangeMin=20),
            color=alt.Color("Industry:N", scale=alt.Scale(range=colors)),
        )
        .properties(height=580)
    )

    arc_chart = base.mark_arc(innerRadius=20, stroke="#fff")

    text_chart = base.mark_text(radiusOffset=10).encode(text="Emissions:Q")

    # Combine arc chart and text chart
    combined_chart = arc_chart + text_chart

    st.altair_chart(combined_chart, use_container_width=True)


def emissions_sources2():
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    emissions = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_CO2_Emissions_Emissions_Intensities_and_"
        """
    )

    emissions = sqldf(
        """
        SELECT "Country", "Industry", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"
        FROM emissions
        """
    )

    # Select relevant columns (including years)
    selected_columns = ["Country", "Industry"] + [
        str(year) for year in range(1995, 2019)
    ]
    emissions_selected = emissions[selected_columns]

    # Melt the DataFrame to reshape it for easier processing
    emissions_melted = pd.melt(
        emissions_selected,
        id_vars=["Country", "Industry"],
        var_name="Year",
        value_name="Emissions",
    )

    # Convert the "Emissions" column to numeric
    emissions_melted["Emissions"] = pd.to_numeric(
        emissions_melted["Emissions"], errors="coerce"
    )

    # Filter for Netherlands, Belgium, Luxembourg, and sum emissions by Industry and Year
    netherlands_belgium_luxembourg = emissions_melted[
        emissions_melted["Country"].isin(["Netherlands", "Belgium", "Luxembourg"])
    ]
    industry_emissions = (
        netherlands_belgium_luxembourg.groupby(["Year", "Industry"])["Emissions"]
        .sum()
        .round(2)
        .reset_index()
    )

    # Get top 10 industries for each year
    top_10_industries = (
        industry_emissions.groupby("Year")
        .apply(lambda x: x.nlargest(10, "Emissions"))
        .reset_index(drop=True)
    )

    years2 = top_10_industries["Year"].unique().tolist()

    option2 = st.selectbox(
        "Please Pick a Year",
        (years2),
        index=10,
        placeholder="Select Year",
        key="option2",
    )

    filtered_data = top_10_industries[top_10_industries["Year"] == str(option2)]

    colors = [
        "#17BEBB",
        "#3590F3",
        "#EF626C",
        "#DFC2F2",
        "#D8D8F6",
        "#c1d7c6",
        "#a3bcf9",
        "#7796cb",
        "#576490",
        "#f6e8ea",
    ]
    # Create Altair chart
    base = (
        alt.Chart(filtered_data)
        .encode(
            alt.Theta("Emissions:Q").stack(True),
            alt.Radius("Emissions:Q").scale(type="sqrt", zero=True, rangeMin=20),
            color=alt.Color("Industry:N", scale=alt.Scale(range=colors)),
        )
        .properties(height=580)
    )

    arc_chart = base.mark_arc(innerRadius=20, stroke="#fff")

    text_chart = base.mark_text(radiusOffset=10).encode(text="Emissions:Q")

    # Combine arc chart and text chart
    combined_chart = arc_chart + text_chart

    st.altair_chart(combined_chart, use_container_width=True)


# 2 columns for main page
col1, col2, col3 = st.columns([8, 1, 8])
with col1:
    st.header("Emissions Per Industry In Selected Year")
    emissions_sources()
with col2:
    st.header(" ")
with col3:
    st.header("Emissions Per Industry In Selected Year")
    emissions_sources2()
