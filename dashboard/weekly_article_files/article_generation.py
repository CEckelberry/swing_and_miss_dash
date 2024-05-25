import pandas as pd
import time
from datetime import datetime
from gemini.gemini_api import generate_gemini_content
from weekly_article_files.prompts import (
    get_top_batters_prompt,
    get_bottom_batters_prompt,
    get_top_starting_pitchers_prompt,
    get_bottom_starting_pitchers_prompt,
    get_top_reliever_pitchers_prompt,
    get_bottom_reliever_pitchers_prompt
)
from weekly_article_files.data_processing import (
    fetch_and_combine_league_avg_batting,
    fetch_and_combine_league_avg_pitching
)

# Function to fill NA values appropriately based on column data types
def fill_na(df):
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(-1)  # Use -1 for numeric columns
        elif pd.api.types.is_categorical_dtype(df[column]):
            df[column] = df[column].cat.add_categories("N/A").fillna("N/A")  # Add "N/A" to categories
        else:
            df[column] = df[column].fillna("N/A")  # Use "N/A" for non-numeric columns
    return df

# Google Gemini API integration for generating content for each section
def generate_section_content(title, dataframe, new_entries, dropped_entries, prompt_function, league_avg):
    dataframe = fill_na(dataframe)
    new_entries = fill_na(new_entries)
    dropped_entries = fill_na(dropped_entries)
    
    data_markdown = dataframe.to_markdown()
    new_entries_markdown = new_entries.to_markdown()
    dropped_entries_markdown = dropped_entries.to_markdown()

    prompt = prompt_function(title, data_markdown, new_entries_markdown, dropped_entries_markdown, league_avg)
    content = generate_gemini_content(prompt)
    return content

# Updated article creation function with Gemini API calls
def create_weekly_article(
    top_starting_pitchers, bottom_starting_pitchers, top_reliever_pitchers, bottom_reliever_pitchers, top_batters, bottom_batters,
    new_top_starting, dropped_top_starting, new_bottom_starting, dropped_bottom_starting,
    new_top_reliever, dropped_top_reliever, new_bottom_reliever, dropped_bottom_reliever,
    new_top_batters, dropped_top_batters, new_bottom_batters, dropped_bottom_batters
):
    season = datetime.now().year
    
    league_avg_batting = fetch_and_combine_league_avg_batting(season)
    league_avg_pitching = fetch_and_combine_league_avg_pitching(season)
    
    top_batters_content = generate_section_content("Top 10 Batters", top_batters, new_top_batters, dropped_top_batters, get_top_batters_prompt, league_avg_batting)
    time.sleep(15)
    top_starting_pitchers_content = generate_section_content("Top 10 Starting Pitchers", top_starting_pitchers, new_top_starting, dropped_top_starting, get_top_starting_pitchers_prompt, league_avg_pitching)
    time.sleep(15)
    top_reliever_pitchers_content = generate_section_content("Top 10 Relief Pitchers", top_reliever_pitchers, new_top_reliever, dropped_top_reliever, get_top_reliever_pitchers_prompt, league_avg_pitching)
    time.sleep(15)
    bottom_batters_content = generate_section_content("Bottom 10 Batters", bottom_batters, new_bottom_batters, dropped_bottom_batters, get_bottom_batters_prompt, league_avg_batting)
    time.sleep(15)
    bottom_starting_pitchers_content = generate_section_content("Bottom 10 Starting Pitchers", bottom_starting_pitchers, new_bottom_starting, dropped_bottom_starting, get_bottom_starting_pitchers_prompt, league_avg_pitching)
    time.sleep(15)
    bottom_reliever_pitchers_content = generate_section_content("Bottom 10 Relief Pitchers", bottom_reliever_pitchers, new_bottom_reliever, dropped_bottom_reliever, get_bottom_reliever_pitchers_prompt, league_avg_pitching)

    article = f"""
    # Weekly Baseball Report

    #### Top 10 Batters
    {top_batters_content}

    #### Top 10 Starting Pitchers
    {top_starting_pitchers_content}

    #### Top 10 Relief Pitchers
    {top_reliever_pitchers_content}

    #### Bottom 10 Batters
    {bottom_batters_content}

    #### Bottom 10 Starting Pitchers
    {bottom_starting_pitchers_content}

    #### Bottom 10 Relief Pitchers
    {bottom_reliever_pitchers_content}
    """
    return article
