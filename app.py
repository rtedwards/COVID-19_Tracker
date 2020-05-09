import streamlit as st
from coronavirus.db_utils.db_utils import DataBase
from coronavirus.utilities.utilities import get_totals, string_of_spaces
from coronavirus.pages.world_map import load_world_map_page
from coronavirus.pages.country_totals import load_country_totals_page


# Display totals
confirmed, deaths, recovered = get_totals()

n_spaces = string_of_spaces(24)
st.markdown(f"\
    ### 🤒 {confirmed:,} {n_spaces}\
        💀 {deaths:,} {n_spaces}\
        🤕 {recovered:,}\n\
            ")

chart_type = st.sidebar.selectbox(label='Page',
                                  options=["Country Totals",
                                           "World Map"])

if chart_type == "Country Totals":
    load_country_totals_page()
if chart_type == "World Map":
    load_world_map_page()

# Sources
# TODO: display_sources() utility function
st.markdown(
    "Sources:  \n\
    [Johns Hopkins](https://github.com/CSSEGISandData/COVID-19) \n\
    [Google](https://www.google.com/covid19/mobility/) \n\
    [World Bank]\
        (api.worldbank.org/v2/en/indicator/EN.POP.DNST?downloadformat=csv) \n\
    ")
st.markdown(
    "Github: [github.com/rtedwards]\
        (https://github.com/rtedwards/coronavirus-tracker)"
)
