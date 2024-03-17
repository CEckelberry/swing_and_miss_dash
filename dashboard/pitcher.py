import streamlit as st
import pandas as pd
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from season_selects.season_selects_avg import season_selectors
from season_selects.season_selects_players import season_selectors_player
from pitcher_selects.pitcher_select import pitcher_select
from pitcher_selects.pitcher_defense import defense
from pitcher_selects.pitchers_df import pitcher_calculator

st.set_page_config(page_title="Pitcher", layout="wide")

add_page_title("Pitcher", layout="wide")

sidebar()


def pitchers():

    st.header("Pitching")

    st.subheader("Pitcher Selection")
    pitcher_select()

    st.subheader("Pitcher Season Selection")
    season_selectors_player()

    st.subheader("Pitcher Metrics")
    pitcher_calculator()

    #st.subheader("Pitcher Defense Metrics")
    #player_field = defense()


pitchers()
