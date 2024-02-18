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
        Page("app.py", "Home", ":city_sunrise:"),
        Page("energy_production.py", "Energy Production", ":factory:"),
        Page("predictions.py", "Solar Production Predictions", ":chart_with_upwards_trend:"),
        Page("position_player.py", "Position Players", ":biohazard_sign:"),
        Page("solar_panels.py", "The number of solar panels needed for the substitution of fossil fuels", ":slot_machine:"),
    ]
)

#2 columns for main page
col1, col2, col3 = st.columns([8,1,8])
with col1:
    st.header("Solar Production Output Benelux Region")
    solar_production()
with col2:
    st.header(" ")
with col3:
    st.header("Greenhouse Gas Emissions Benelux Region")
    ghg_emissions()