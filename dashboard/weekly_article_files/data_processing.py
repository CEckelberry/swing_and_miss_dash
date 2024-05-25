import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
import os

from weekly_article_files.config import min_pa, min_starter_ip, min_reliever_ip, max_reliever_ip

# Directory to save the weekly data
DATA_DIR = "weekly_article_files/data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Add new functions to fetch league average stats
def fetch_and_combine_league_avg_batting(season):
    advanced = fetch_data(f"SELECT * FROM `swingandmiss.league_avg_batting.advanced` WHERE Season={season}")
    standard = fetch_data(f"SELECT * FROM `swingandmiss.league_avg_batting.standard` WHERE Season={season}")
    combined = pd.merge(advanced, standard, on='Season', suffixes=('_advanced', '_standard'))
    combined = combined.loc[:, ~combined.columns.duplicated()]  # Remove duplicate columns
    return combined
# Add new functions to fetch league average stats
def fetch_and_combine_league_avg_pitching(season):
    advanced = fetch_data(f"SELECT * FROM `swingandmiss.league_avg_pitching.advanced` WHERE Season={season}")
    standard = fetch_data(f"SELECT * FROM `swingandmiss.league_avg_pitching.standard` WHERE Season={season}")
    combined = pd.merge(advanced, standard, on='Season', suffixes=('_advanced', '_standard'))
    combined = combined.loc[:, ~combined.columns.duplicated()]  # Remove duplicate columns
    return combined


# Credentials and client setup
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials)

# Function to fetch data based on the query
def fetch_data(query):
    return pd.read_gbq(query, credentials=credentials, dialect='standard')

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

# Function to save data to a CSV file
def save_data(df, filename):
    df.to_csv(os.path.join(DATA_DIR, filename), index=False)

# Function to load data from a CSV file
def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame()
