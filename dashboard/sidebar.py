import streamlit as st
from PIL import Image
from pandasql import sqldf
import pandas as pd

import warnings

# Suppress FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)


def sidebar():
    with st.sidebar:
        image = Image.open("./images/swingandmisslogo.png")
        st.image(image, output_format="auto")
      