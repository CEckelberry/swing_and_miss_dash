import streamlit as st
import pandas as pd
import altair as alt
from st_pages import Page, show_pages, add_page_title
from sidebar import sidebar

# Suppress SettingWithCopyWarning
pd.options.mode.chained_assignment = None  # default='warn'

add_page_title(
    "The number of solar panels needed for the substitution of fossil fuels",
    layout="wide",
)


def solar_panels():
    sidebar()
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    solar_panels_df = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_energy_production_benelux" 
        """
    )

    # Filtering data for fossil fuels and solar
    fossil_fuels_df = solar_panels_df[
        solar_panels_df["Product"].str.contains(
            "Fuels|Coal|Oil|Gas", case=False, regex=True
        )
    ]
    solar_df = solar_panels_df[
        solar_panels_df["Product"].str.contains("Solar", case=False, regex=True)
    ]

    # Convert 'Value' column to numeric
    fossil_fuels_df["Value"] = pd.to_numeric(fossil_fuels_df["Value"])
    solar_df["Value"] = pd.to_numeric(solar_df["Value"])

    # Calculate the total electricity production from fossil fuels and solar panels
    total_fossil_fuels = round(fossil_fuels_df["Value"].sum(), 2)
    total_solar_energy = round(solar_df["Value"].sum(), 2)

    # Conversion constant
    gwh_to_wh = 1000000000  # GWh to watt-hours

    # Convert total electricity production to watt-hours
    total_fossil_fuels_watts = total_fossil_fuels * gwh_to_wh

    # Calculate the number of solar panels needed, assuming that one solar panel produces 400 watt energy
    number_of_solar_panels = int(total_fossil_fuels_watts / 400)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            f"<p style='text-align:center;'>Please select wattage (between 250 and 500)</p>",
            unsafe_allow_html=True,
        )

        # Slider for selecting the wattage
        selected_wattage = st.slider("", 250, 500, 400)

        # Calculate the number of solar panels needed, based on the selected wattage
        number_of_solar_panels = int(total_fossil_fuels_watts / selected_wattage)

        formatted_number_of_solar_panels = f"{number_of_solar_panels:,}"
        
        st.markdown(f"<p style='text-align:center;'>Based on the data and the selected wattage ({selected_wattage} watts), the number of solar panels needed to replace fossil fuels is calculated</p>",
            unsafe_allow_html=True
        )

        st.markdown(f"<div style='display: flex; flex-direction: column; align-items: center; width: 350px; background-color:#e6f3ff;padding:5px;border-radius:10px; margin: auto;'> <p style='font-size:18px;font-weight:bold;margin-bottom:0px;'>Number of Solar Panels Needed</p> <p style='font-size:24px;font-weight:bold;margin-top:0px;'>{formatted_number_of_solar_panels}</p> </div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div style='text-align: justify; background-color: #f9f9f9; padding: 20px; border-radius: 10px;'>
                <p style='font-size: 18px;'>\U0001F4A1<span style='margin-left: 10px'>Outlined here is an estimate of the required solar panels to entirely substitute fossil fuels in Benelux.</span></p>
                <p style='font-size: 18px;'>Solar panel performance is significantly influenced by wattage, where higher wattage panels generate more power. Residential solar panels typically range from 250 to 400 watts, with the most efficient models offering 370 to 445 watts. Higher wattage translates to increased energy output, reducing the number of panels needed for the same power generation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='text-align: center;margin-top: 30px;'><h3>Comparison of Electricity Production from Fossil Fuels and Solar Energy</h3></div>",
        unsafe_allow_html=True,
    )

    data = pd.DataFrame(
        {
            "Energy Source": ["Fossil Fuels", "Solar Energy"],
            "Electricity Production (GWh)": [total_fossil_fuels, total_solar_energy],
        }
    )

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Electricity Production (GWh)", title="Electricity Production (GWh)"
            ),
            y=alt.Y("Energy Source", title=None),
            color=alt.Color(
                "Energy Source", scale=alt.Scale(range=["#17BEBB", "#3590F3"])
            ),
        )
        .properties(width=700, height=500)
    )

    st.write(chart)


solar_panels()