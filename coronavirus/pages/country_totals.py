import altair as alt
import streamlit as st
import numpy as np
from coronavirus.db_utils.db_utils import DataBase
from coronavirus.preprocessor.preprocessor import (consolidate_country_regions,
                                                   get_top_n_countries)
from coronavirus.utilities.utilities import (add_column_cases_per_day,
                                             add_ISO2_country_codes,
                                             add_ISO3_country_codes,
                                             add_country_population,
                                             add_population_density,
                                             add_google_mobility_data,
                                             rolling_mean)


def load_country_totals_page():
    # Get the data
    db = DataBase('COVID-19.db')
    data_type = st.sidebar.selectbox(label='Select data', options=['DEATHS', 'CONFIRMED', 'RECOVERED'], index=0)

    if data_type == 'CONFIRMED':
        response = 'confirmed'
        df = db.read_table_to_dataframe('jh_global_confirmed', response)
        # df = db.load_jh_world_df()
    elif data_type == 'DEATHS':
        response = 'deaths'
        df = db.read_table_to_dataframe('jh_global_deaths', response)
        # df = db.load_jh_world_df()
    else:
        response = 'recovered'
        df = db.read_table_to_dataframe('jh_global_recovered', response)
        # df = db.load_jh_world_df()

    # Select Country row by dropping all rows where province/state != None
    st.header("Countries over Time")
    df = consolidate_country_regions(df)

    n = st.sidebar.number_input(label='Top number of countries to plot',
                                min_value=1,
                                value=5)

    top_countries = get_top_n_countries(df, n, response)
    selected_countries = st.sidebar.multiselect(
        'Select countries',
        list(df['country/region'].sort_values().unique()),
        default=top_countries
    )

    log_scale = st.sidebar.checkbox("Log Scale", value=False)
    smooth = st.sidebar.checkbox("Smooth", value=False)  # Running 7 day average

    # TODO: scale df to date of x number of cases
    # x_num_cases = st.sidebar.checkbox("Days Since 10,000 Cases")

    # Create new columns
    response_rate = response + '_per_day'
    df = add_column_cases_per_day(df, response, response_rate)
    df = add_ISO2_country_codes(df)
    df = add_ISO3_country_codes(df)
    # df = add_country_population(df)
    df = add_population_density(df)
    # df = add_google_mobility_data(df)
    # df = df.dropna()

    countries_df = df[df['country/region'].isin(selected_countries)]

    if smooth:  # Apply rolling average over 7 days
        num_days = 7
        countries_df[response] = countries_df.sort_values(
            ['country/region', 'date'], ascending=True).groupby('country/region')[response].transform(lambda x: rolling_mean(x, num_days))
        countries_df[response_rate] = countries_df.sort_values(
            ['country/region', 'date'], ascending=True).groupby('country/region')[response_rate].transform(lambda x: rolling_mean(x, num_days))

    if log_scale:
        # Remove rows with 0 response because log(0) is undefined
        log_df = countries_df.loc[countries_df[response] > 0]
        log_rate_df = countries_df.loc[countries_df[response_rate] > 0]

        totals_plot = alt.Chart(log_df).mark_line(interpolate='basis').encode(
            alt.Y(response + ':Q', scale=alt.Scale(type='log')),
            x='date' + ':T',
            color='country/region' + ':N'
        )
        rates_plot = alt.Chart(log_rate_df).mark_line(interpolate='basis').encode(
            alt.Y(response_rate + ':Q',
                  scale=alt.Scale(type='log')),
            x='date' + ':T',
            color='country/region' + ':N'
        )
    else:
        totals_plot = alt.Chart(countries_df).mark_line(interpolate='basis').encode(
            x='date' + ':T',
            y=response + ':Q',
            color='country/region' + ':N'
        )
        rates_plot = alt.Chart(countries_df).mark_line(interpolate='basis').encode(
            x='date' + ':T',
            y=response_rate + ':Q',
            color='country/region' + ':N'
        )

    st.altair_chart(totals_plot, use_container_width=True)
    st.altair_chart(rates_plot, use_container_width=True)

    if log_scale:
        st.markdown(
            f"* Removed rows with `{response_rate}` \
              less than or equal to 0 because:  \n\
              $log(x)$ is undefined when $x \leq 0$")

    # Show data table for most recent date
    current_date = df['date'].max()
    st.write(countries_df[countries_df['date'] == current_date])
