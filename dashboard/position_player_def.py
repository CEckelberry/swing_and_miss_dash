import streamlit as st
import pandas as pd
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from season_selects.season_selects_avg import season_selectors
from season_selects.season_selects_players import season_selectors_player
from player_selects.player_select import player_select
from player_selects.player_defense import defense


add_page_title("Position Player", layout="wide")

sidebar()


def position_players_def():

    st.header("Fielding")

    st.subheader("League Average Selections")
    season_selectors()

    st.subheader("Player Selection")
    player_select()

    st.subheader("Player Season Selection")
    season_selectors_player()

    player_field = defense()


position_players_def()
