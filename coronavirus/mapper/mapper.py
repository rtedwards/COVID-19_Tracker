import folium
import geopandas as gpd
import joblib
import json
import os
import pandas as pd
import urllib

URL = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'

COUNTRY_GEO = f'https://github.com/datasets/geo-countries/tree/master/data/countries.geojson'
COUNTRY_GEO = f'{URL}/world-countries.json'
STATE_GEO = f'{URL}/us-states.json'

# Alternate geojson
# https://geojson-maps.ash.ms/

def choropleth_map(df,columns,geo_data,color,legend):
    cmap = folium.Map(location=[48, -102], 
                      tiles='OpenStreetMap',
                      zoom_start=4,
                      min_zoom=4,
                      max_zoom=15)

    folium.Choropleth(geo_data=geo_data,
                      name='choropleth',
                      data=df,
                    #   columns=['ISO3 Code', 'confirmed'],
                      columns=columns,
                      key_on='feature.id',
                      fill_color=color,
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      legend_name=legend,
                      show=False
    ).add_to(cmap)

    folium.TileLayer('Stamen Terrain').add_to(cmap)
    folium.TileLayer('MapQuest Open Aerial', attr="MapQuest Open Aerial").add_to(cmap)
    folium.TileLayer('cartodbdark_matter').add_to(cmap)
    folium.TileLayer('stamentoner').add_to(cmap)
    folium.LayerControl().add_to(cmap)

    return cmap
