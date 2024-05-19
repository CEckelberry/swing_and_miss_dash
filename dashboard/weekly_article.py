import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import datetime
from gemini.gemini_api import generate_gemini_content

# Constants
SEASON_START = datetime.date(datetime.datetime.now().year, 4, 1)
SEASON_END = datetime.date(datetime.datetime.now().year, 10, 8)
AVERAGE_PA = 550
AVERAGE_STARTER_IP = 180  # Average IP for starting pitchers
AVERAGE_RELIEVER_IP = 60  # Average IP for relief pitchers

# Calculate season progress
today = datetime.date.today()
season_days_total = (SEASON_END - SEASON_START).days
season_days_elapsed = (today - SEASON_START).days
season_progress = season_days_elapsed / season_days_total

# Calculate dynamic minimum PA and IP
min_pa = round(AVERAGE_PA * season_progress)
min_starter_ip = round(AVERAGE_STARTER_IP * season_progress)
min_reliever_ip = round(AVERAGE_RELIEVER_IP * season_progress)
max_reliever_ip = min_reliever_ip + 5  # Adding a small range to consider upper limit

# Credentials and client setup
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials)

# Get the current year
current_year = datetime.datetime.now().year
season = current_year

# Function to fetch data based on the query
def fetch_data(query):
    return pd.read_gbq(query, credentials=credentials, dialect='standard')

# Define queries for top and bottom starting pitchers
top_10_starting_pitchers_query = f"""
WITH ranked_pitchers AS (
    SELECT 
        `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
        `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
        `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
        `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
        ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` ASC) AS row_num
    FROM 
        `raw_data`.`pitching_stats`
    WHERE
        `Season` = {season} AND `IP` > {min_starter_ip}
)
SELECT * EXCEPT(row_num)
FROM ranked_pitchers
WHERE row_num = 1
ORDER BY `SIERA` ASC
LIMIT 10
"""

bottom_10_starting_pitchers_query = f"""
WITH ranked_pitchers AS (
    SELECT 
        `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
        `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
        `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
        `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
        ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` DESC) AS row_num
    FROM 
        `raw_data`.`pitching_stats`
    WHERE
        `Season` = {season} AND `IP` > {min_starter_ip}
)
SELECT * EXCEPT(row_num)
FROM ranked_pitchers
WHERE row_num = 1
ORDER BY `SIERA` DESC
LIMIT 10
"""

# Define queries for top and bottom relief pitchers
top_10_reliever_pitchers_query = f"""
WITH ranked_relievers AS (
    SELECT 
        `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
        `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
        `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
        `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
        ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` ASC) AS row_num
    FROM 
        `raw_data`.`pitching_stats`
    WHERE
        `Season` = {season} AND `IP` BETWEEN {min_reliever_ip} AND {max_reliever_ip}
)
SELECT * EXCEPT(row_num)
FROM ranked_relievers
WHERE row_num = 1
ORDER BY `SIERA` ASC
LIMIT 10
"""

bottom_10_reliever_pitchers_query = f"""
WITH ranked_relievers AS (
    SELECT 
        `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
        `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
        `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
        `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
        ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` DESC) AS row_num
    FROM 
        `raw_data`.`pitching_stats`
    WHERE
        `Season` = {season} AND `IP` BETWEEN {min_reliever_ip} AND {max_reliever_ip}
)
SELECT * EXCEPT(row_num)
FROM ranked_relievers
WHERE row_num = 1
ORDER BY `SIERA` DESC
LIMIT 10
"""

# Define queries for top and bottom batters
top_10_batters_query = f"""
WITH ranked_batters AS (
    SELECT 
        `Season`, `Name`, ROUND(`AVG`, 3) AS `AVG`, ROUND(`OBP`, 3) AS `OBP`, ROUND(`SLG`, 3) AS `SLG`, 
        `wRC_`, ROUND(`wOBA`, 3) AS `wOBA`, ROUND(`OPS`, 3) AS `OPS`, ROUND(`BABIP`, 3) AS `BABIP`, `WAR`, 
        `K_` AS `K%`, `BB_` AS `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`, `3B` AS `Triples`, `2B` AS `Doubles`, 
        `RBI`, `H` AS `Hits`, `Age`, `G`, `PA`,
        ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `wRC_` DESC) AS row_num
    FROM 
        `raw_data`.`batting_stats`
    WHERE
        `Season` = {season} AND `PA` >= {min_pa}
)
SELECT 
    `Season`, `Name`, `AVG`, `OBP`, `SLG`, `wRC_` AS `wRC+`, `wOBA`, `OPS`, `BABIP`, `WAR`, `K%`, `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`,
    `Triples`, `Doubles`, `RBI`, `Hits`, `Age`, `G`, `PA`
FROM ranked_batters
WHERE row_num = 1
ORDER BY `wRC+` DESC
LIMIT 10
"""

bottom_10_batters_query = f"""
WITH ranked_batters AS (
    SELECT 
        `Season`, `Name`, ROUND(`AVG`, 3) AS `AVG`, ROUND(`OBP`, 3) AS `OBP`, ROUND(`SLG`, 3) AS `SLG`, 
        `wRC_`, ROUND(`wOBA`, 3) AS `wOBA`, ROUND(`OPS`, 3) AS `OPS`, ROUND(`BABIP`, 3) AS `BABIP`, `WAR`, 
        `K_` AS `K%`, `BB_` AS `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`, `3B` AS `Triples`, `2B` AS `Doubles`, 
        `RBI`, `H` AS `Hits`, `Age`, `G`, `PA`,
        ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `wRC_` ASC) AS row_num
    FROM 
        `raw_data`.`batting_stats`
    WHERE
        `Season` = {season} AND `PA` >= {min_pa}
)
SELECT 
    `Season`, `Name`, `AVG`, `OBP`, `SLG`, `wRC_` AS `wRC+`, `wOBA`, `OPS`, `BABIP`, `WAR`, `K%`, `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`,
    `Triples`, `Doubles`, `RBI`, `Hits`, `Age`, `G`, `PA`
FROM ranked_batters
WHERE row_num = 1
ORDER BY `wRC+` ASC
LIMIT 10
"""

# Google Gemini API integration for generating content for each section
def generate_section_content(title, dataframe):
    data_markdown = dataframe.to_markdown()
    prompt = f"{title}:\n{data_markdown}\nProvide a summary and analysis of the above data."
    content = generate_gemini_content(prompt)
    return content

# Updated article creation function with Gemini API calls
def create_weekly_article(top_starting_pitchers, bottom_starting_pitchers, top_reliever_pitchers, bottom_reliever_pitchers, top_batters, bottom_batters):
    top_starting_pitchers_content = generate_section_content("Top 10 Starting Pitchers", top_starting_pitchers)
    bottom_starting_pitchers_content = generate_section_content("Bottom 10 Starting Pitchers", bottom_starting_pitchers)
    top_reliever_pitchers_content = generate_section_content("Top 10 Relief Pitchers", top_reliever_pitchers)
    bottom_reliever_pitchers_content = generate_section_content("Bottom 10 Relief Pitchers", bottom_reliever_pitchers)
    top_batters_content = generate_section_content("Top 10 Batters", top_batters)
    bottom_batters_content = generate_section_content("Bottom 10 Batters", bottom_batters)

    article = f"""
    # Weekly Baseball Report

    ## Top 10 Starting Pitchers
    {top_starting_pitchers_content}

    ## Bottom 10 Starting Pitchers
    {bottom_starting_pitchers_content}

    ## Top 10 Relief Pitchers
    {top_reliever_pitchers_content}

    ## Bottom 10 Relief Pitchers
    {bottom_reliever_pitchers_content}

    ## Top 10 Batters
    {top_batters_content}

    ## Bottom 10 Batters
    {bottom_batters_content}
    """
    return article

# Function to format specified columns to desired decimal places
def format_columns(df):
    columns_to_format = {
        'AVG': '{:.3f}',
        'OBP': '{:.3f}',
        'SLG': '{:.3f}',
        'OPS': '{:.3f}',
        'BABIP': '{:.3f}',
        'IP': '{:.1f}',
        'SIERA': '{:.2f}',
        'xFIP': '{:.2f}',
        'GB%': '{:.1f}',
        'K%': '{:.1f}',
        'BB%': '{:.1f}',
        'SwStr%': '{:.1f}',
        'LOB%': '{:.1f}'
    }
    for column, format_spec in columns_to_format.items():
        if column in df.columns:
            df[column] = df[column].apply(lambda x: format_spec.format(x) if pd.notnull(x) else x)
    return df

# Function to convert decimal columns to percentages
def convert_to_percentage(df):
    columns_to_convert = ['GB%', 'K%', 'BB%', 'SwStr%', 'LOB%']
    for column in columns_to_convert:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: x * 100)
    return df

# Generate weekly article button
if st.button("Generate Weekly Baseball Article"):
    # Fetching data
    top_starting_pitchers = fetch_data(top_10_starting_pitchers_query)
    bottom_starting_pitchers = fetch_data(bottom_10_starting_pitchers_query)
    top_reliever_pitchers = fetch_data(top_10_reliever_pitchers_query)
    bottom_reliever_pitchers = fetch_data(bottom_10_reliever_pitchers_query)
    top_batters = fetch_data(top_10_batters_query)
    bottom_batters = fetch_data(bottom_10_batters_query)

    # Converting to percentage
    top_starting_pitchers = convert_to_percentage(top_starting_pitchers)
    bottom_starting_pitchers = convert_to_percentage(bottom_starting_pitchers)
    top_reliever_pitchers = convert_to_percentage(top_reliever_pitchers)
    bottom_reliever_pitchers = convert_to_percentage(bottom_reliever_pitchers)

    # Formatting data
    top_starting_pitchers = format_columns(top_starting_pitchers)
    bottom_starting_pitchers = format_columns(bottom_starting_pitchers)
    top_reliever_pitchers = format_columns(top_reliever_pitchers)
    bottom_reliever_pitchers = format_columns(bottom_reliever_pitchers)
    top_batters = format_columns(top_batters)
    bottom_batters = format_columns(bottom_batters)

    # Ensure Season is presented correctly
    for df in [top_starting_pitchers, bottom_starting_pitchers, top_reliever_pitchers, bottom_reliever_pitchers, top_batters, bottom_batters]:
        if 'Season' in df.columns:
            df['Season'] = df['Season'].astype(str)

    # Displaying data
    st.write("## Weekly Baseball Report")
    
    st.write("### Top 10 Starting Pitchers")
    st.dataframe(top_starting_pitchers)

    st.write("### Bottom 10 Starting Pitchers")
    st.dataframe(bottom_starting_pitchers)
    
    st.write("### Top 10 Relief Pitchers")
    st.dataframe(top_reliever_pitchers)

    st.write("### Bottom 10 Relief Pitchers")
    st.dataframe(bottom_reliever_pitchers)

    st.write("### Top 10 Batters")
    st.dataframe(top_batters)

    st.write("### Bottom 10 Batters")
    st.dataframe(bottom_batters)

    # Generating article
    weekly_article = create_weekly_article(top_starting_pitchers, bottom_starting_pitchers, top_reliever_pitchers, bottom_reliever_pitchers, top_batters, bottom_batters)
    st.markdown(weekly_article)
