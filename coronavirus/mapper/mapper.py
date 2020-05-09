import folium

URL = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
COUNTRY_GEO = f'https://github.com/datasets/geo-countries/tree/master/data/countries.geojson'
COUNTRY_GEO = f'{URL}/world-countries.json'
STATE_GEO = f'{URL}/us-states.json'

# Alternate geojson
# https://geojson-maps.ash.ms/


def choropleth_map(df, columns, geo_data, color, legend):
    bmap = folium.Map(location=[48, -102],
                      tiles='OpenStreetMap',
                      attr='www.openstreetmap.com',
                      zoom_start=4,
                      min_zoom=2,
                      max_zoom=15
                      )

    cmap = folium.Choropleth(geo_data=geo_data,
                             name='choropleth',
                             data=df,
                             # columns=['ISO3 Code', 'confirmed'],
                             columns=columns,
                             key_on='feature.id',
                             fill_color=color,
                             fill_opacity=0.7,
                             line_opacity=0.2,
                             legend_name=legend,
                             show=False)
    # ).add_to(cmap)

    bmap.add_child(cmap)

    # folium.TileLayer('Stamen Terrain').add_to(cmap)
    # folium.TileLayer('MapQuest Open Aerial', attr="MapQuest Open Aerial").add_to(cmap)
    # folium.TileLayer('cartodbdark_matter').add_to(cmap)
    # folium.TileLayer('stamentoner').add_to(cmap)
    # folium.LayerControl().add_to(cmap)

    return bmap


def base_map():
    """Simple base map"""
    bmap = folium.Map([50.848633, 4.3497730],
                      zoom_start=15,
                      control_scale=True,
                      tiles='cartodbpositron')
    return bmap
