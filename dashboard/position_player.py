import altair as alt
import streamlit as st
from pandasql import sqldf
import pandas as pd
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from google.oauth2 import service_account
from google.cloud import bigquery
from season_selects.season_selects_avg import season_selectors
from season_selects.season_selects_players import season_selectors_player
from player_selects.player_select import player_select
from player_selects.players_df import player_calculator


add_page_title("Position Player", layout="wide")

sidebar()


def position_players():

    st.header("Batting")

    st.subheader("League Average Selections")
    season_selectors()

    st.subheader("Player Selection")
    player_select()

    st.subheader("Player Season Selection")
    season_selectors_player()

    st.subheader("Mashed Results")
    player_comp = player_calculator()

    st.header("Fielding")

    st.subheader("DRS")

    st.subheader("UZR")

    st.subheader("UZR_150")

    st.subheader("Def")

    st.subheader("OAA")


position_players()
