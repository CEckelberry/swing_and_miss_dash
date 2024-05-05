import streamlit as st
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from emissions import ghg_emissions

# Optional -- adds the title and icon to the current page
add_page_title("Swing And Miss Comparison App", layout="wide")

sidebar()

# Specify what pages should be shown in the sidebar
show_pages(
    [
        Page("app.py", "Home", ":globe_with_meridians:"),
        Page("weekly_article.py", "Weekly Article", ":globe_with_meridians:"),
        Page("team_hitting.py", "Team Batting", ":us:"),
        Page("team_fielding.py", "Team Fielding", ":stadium:"),
        Page("team_pitching.py", "Team Pitching", ":trophy:"),
        Page("position_player_off.py", "Position Player Offense", ":sports_medal:"),
        Page("position_player_def.py", "Position Player Defense", ":corn:"),
        Page("pitcher.py", "Pitcher", ":baseball:"),
    ]
)
