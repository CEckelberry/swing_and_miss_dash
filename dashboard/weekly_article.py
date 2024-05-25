import streamlit as st
from datetime import datetime, date, timedelta
from weekly_article_files import queries
from weekly_article_files import data_processing
from weekly_article_files import article_generation
from weekly_article_files.config import min_pa, min_starter_ip, min_reliever_ip, max_reliever_ip
import pandas as pd

# Calculate date ranges for current and previous week
today = date.today()
current_week_start = today - timedelta(days=7)
current_week_end = today
previous_week_start = today - timedelta(days=14)
previous_week_end = today - timedelta(days=7)

# Get the current year
current_year = datetime.now().year
season = current_year

# Compare current data with previous week's data
def compare_with_previous(current_data, previous_data):
    if 'Name' not in current_data.columns or 'Name' not in previous_data.columns:
        raise KeyError("The 'Name' column is missing from one of the dataframes.")
    merged = current_data.merge(previous_data, on='Name', suffixes=('', '_previous'), how='outer', indicator=True)
    new_entries = merged[merged['_merge'] == 'left_only']
    dropped_entries = merged[merged['_merge'] == 'right_only']
    return new_entries, dropped_entries

# Generate weekly article button
if st.button("Generate Weekly Baseball Article"):
    # Fetching data for current week
    top_starting_pitchers = data_processing.fetch_data(queries.get_top_starting_pitchers_query(season, min_starter_ip, current_week_start, current_week_end))
    bottom_starting_pitchers = data_processing.fetch_data(queries.get_bottom_starting_pitchers_query(season, min_starter_ip, current_week_start, current_week_end))
    top_reliever_pitchers = data_processing.fetch_data(queries.get_top_reliever_pitchers_query(season, min_reliever_ip, max_reliever_ip, current_week_start, current_week_end))
    bottom_reliever_pitchers = data_processing.fetch_data(queries.get_bottom_reliever_pitchers_query(season, min_reliever_ip, max_reliever_ip, current_week_start, current_week_end))
    top_batters = data_processing.fetch_data(queries.get_top_batters_query(season, min_pa, current_week_start, current_week_end))
    bottom_batters = data_processing.fetch_data(queries.get_bottom_batters_query(season, min_pa, current_week_start, current_week_end))

    # Fetching data for previous week
    prev_top_starting_pitchers = data_processing.fetch_data(queries.get_top_starting_pitchers_query(season, min_starter_ip, previous_week_start, previous_week_end))
    prev_bottom_starting_pitchers = data_processing.fetch_data(queries.get_bottom_starting_pitchers_query(season, min_starter_ip, previous_week_start, previous_week_end))
    prev_top_reliever_pitchers = data_processing.fetch_data(queries.get_top_reliever_pitchers_query(season, min_reliever_ip, max_reliever_ip, previous_week_start, previous_week_end))
    prev_bottom_reliever_pitchers = data_processing.fetch_data(queries.get_bottom_reliever_pitchers_query(season, min_reliever_ip, max_reliever_ip, previous_week_start, previous_week_end))
    prev_top_batters = data_processing.fetch_data(queries.get_top_batters_query(season, min_pa, previous_week_start, previous_week_end))
    prev_bottom_batters = data_processing.fetch_data(queries.get_bottom_batters_query(season, min_pa, previous_week_start, previous_week_end))

    # Ensure 'Name' column exists and is correctly named
    for df, name in zip(
        [top_starting_pitchers, bottom_starting_pitchers, top_reliever_pitchers, bottom_reliever_pitchers, top_batters, bottom_batters],
        ["top_starting_pitchers", "bottom_starting_pitchers", "top_reliever_pitchers", "bottom_reliever_pitchers", "top_batters", "bottom_batters"]
    ):
        if 'Name' not in df.columns:
            st.error(f"The 'Name' column is missing from {name} data.")
            st.stop()

    # Converting to percentage
    top_starting_pitchers = data_processing.convert_to_percentage(top_starting_pitchers)
    bottom_starting_pitchers = data_processing.convert_to_percentage(bottom_starting_pitchers)
    top_reliever_pitchers = data_processing.convert_to_percentage(top_reliever_pitchers)
    bottom_reliever_pitchers = data_processing.convert_to_percentage(bottom_reliever_pitchers)

    # Formatting data
    top_starting_pitchers = data_processing.format_columns(top_starting_pitchers)
    bottom_starting_pitchers = data_processing.format_columns(bottom_starting_pitchers)
    top_reliever_pitchers = data_processing.format_columns(top_reliever_pitchers)
    bottom_reliever_pitchers = data_processing.format_columns(bottom_reliever_pitchers)
    top_batters = data_processing.format_columns(top_batters)
    bottom_batters = data_processing.format_columns(bottom_batters)

    # Ensure 'Name' column exists in previous week's data
    for df, name in zip(
        [prev_top_starting_pitchers, prev_bottom_starting_pitchers, prev_top_reliever_pitchers, prev_bottom_reliever_pitchers, prev_top_batters, prev_bottom_batters],
        ["prev_top_starting_pitchers", "prev_bottom_starting_pitchers", "prev_top_reliever_pitchers", "prev_bottom_reliever_pitchers", "prev_top_batters", "prev_bottom_batters"]
    ):
        if 'Name' not in df.columns:
            st.error(f"The 'Name' column is missing from {name} data.")
            st.stop()

    # Compare current data with previous week's data
    new_top_starting, dropped_top_starting = compare_with_previous(top_starting_pitchers, prev_top_starting_pitchers)
    new_bottom_starting, dropped_bottom_starting = compare_with_previous(bottom_starting_pitchers, prev_bottom_starting_pitchers)
    new_top_reliever, dropped_top_reliever = compare_with_previous(top_reliever_pitchers, prev_top_reliever_pitchers)
    new_bottom_reliever, dropped_bottom_reliever = compare_with_previous(bottom_reliever_pitchers, prev_bottom_reliever_pitchers)
    new_top_batters, dropped_top_batters = compare_with_previous(top_batters, prev_top_batters)
    new_bottom_batters, dropped_bottom_batters = compare_with_previous(bottom_batters, prev_bottom_batters)

    # Ensure Season is presented correctly
    for df in [top_starting_pitchers, bottom_starting_pitchers, top_reliever_pitchers, bottom_reliever_pitchers, top_batters, bottom_batters]:
        if 'Season' in df.columns:
            df['Season'] = df['Season'].astype(str)

    # Create dictionary of tables
    tables_dict = {
        "Top 10 Batters": top_batters,
        "Top 10 Starting Pitchers": top_starting_pitchers,
        "Top 10 Relief Pitchers": top_reliever_pitchers,
        "Bottom 10 Batters": bottom_batters,
        "Bottom 10 Starting Pitchers": bottom_starting_pitchers,
        "Bottom 10 Relief Pitchers": bottom_reliever_pitchers
    }

    # Displaying data as HTML tables
    st.write("## Weekly Baseball Report")
    
    for i, (title, table) in enumerate(tables_dict.items(), start=1):
        table_html = table.to_html(index=False)
        div_html = f'<div id="weekly_table_{i}">{table_html}</div>'
        st.subheader(title)
        st.markdown(div_html, unsafe_allow_html=True)

        # Collapsible code block and copy button
        st.markdown(f"""
            <details>
                <summary>Show HTML</summary>
                <textarea id="table_html_{i}" style="width: 100%; height: 100px;">{div_html}</textarea>
            </details>
            <button onclick="navigator.clipboard.writeText(document.getElementById('table_html_{i}').value)">Copy to Clipboard</button>
        """, unsafe_allow_html=True)

        st.divider()

    # Generating article
    weekly_article = article_generation.create_weekly_article(
        top_starting_pitchers, bottom_starting_pitchers, top_reliever_pitchers, bottom_reliever_pitchers, top_batters, bottom_batters,
        new_top_starting, dropped_top_starting, new_bottom_starting, dropped_bottom_starting,
        new_top_reliever, dropped_top_reliever, new_bottom_reliever, dropped_bottom_reliever,
        new_top_batters, dropped_top_batters, new_bottom_batters, dropped_bottom_batters
    )
    st.markdown(weekly_article)

    # Save current data for next week's comparison
    data_processing.save_data(top_starting_pitchers, "top_starting_pitchers.csv")
    data_processing.save_data(bottom_starting_pitchers, "bottom_starting_pitchers.csv")
    data_processing.save_data(top_reliever_pitchers, "top_reliever_pitchers.csv")
    data_processing.save_data(bottom_reliever_pitchers, "bottom_reliever_pitchers.csv")
    data_processing.save_data(top_batters, "top_batters.csv")
    data_processing.save_data(bottom_batters, "bottom_batters.csv")
