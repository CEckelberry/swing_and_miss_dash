import streamlit as st
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from solar_production import solar_production
from emissions import ghg_emissions

# Optional -- adds the title and icon to the current page
add_page_title("Swing And Miss Comparison App", layout="wide")

sidebar()

# Specify what pages should be shown in the sidebar
show_pages(
    [
        Page("app.py", "Home", ":baseball:"),
        Page("energy_production.py", "Team Batting", ":stadium:"),
        Page("energy_production.py", "Team Fielding", ":stadium:"),
        Page("predictions.py", "Team Pitching", ":trophy:"),
        Page("position_player_off.py", "Position Player Offense", ":sports_medal:"),
        Page("position_player_def.py", "Position Player Defense", ":baseball:"),
        Page("pitcher.py", "Pitcher", ":baseball:"),
    ]
)
