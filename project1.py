import folium
from folium.plugins import Fullscreen
import geopandas as gpd
import pandas as pd


gdf =gpd.read_file(r"C:\Users\User\.vscode\.vscode\python\gropandas\gadm41_BGD_1.json.zip")

gdf_geo =gdf.to_crs(epsg=32646).to_crs(epsg=4326)

population_df = pd.DataFrame({
    'NAME_1': ['Barisal', 'Chittagong', 'Dhaka', 'Khulna',
               'Rajshahi', 'Rangpur', 'Sylhet', 'Mymensingh'],
    'population': [8, 33, 36, 16, 21, 16, 10, 12]
})

merged =gdf_geo.merge(population_df,on="NAME_1")

def style_function(feature):
    pop = feature['properties']['population']
    if pop > 30:
        color = '#800026'
    elif pop > 15:
        color = '#fd8d3c'
    else:
        color = '#ffffb2'
    return {'fillColor': color, 'color': 'black', 'weight': 1, 'fillOpacity': 0.7}

m = folium.Map(location=[23.685, 90.3563], zoom_start=7)

choropleth_layer =folium.FeatureGroup(name="population mohai choroleth")

folium.GeoJson(
    merged,
    style_function= style_function,
    tooltip=folium.GeoJsonTooltip(fields=['NAME_1', 'population'],
                                  aliases=['Division:', 'Population (millions):'])
).add_to(choropleth_layer)

choropleth_layer.add_to(m)

markers_layer = folium.FeatureGroup(name="Major Cities")
cities = [
    {"name": "Dhaka", "lat": 23.8103, "lon": 90.4125, "population": 36},
    {"name": "Chittagong", "lat": 22.3569, "lon": 91.7832, "population": 33},
    {"name": "Sylhet", "lat": 24.8949, "lon": 91.8687, "population": 10},
    {"name": "Rajshahi", "lat": 24.3745, "lon": 88.6042, "population": 21},
    {"name": "Pabna", "lat": 24.0064, "lon": 89.2372, "population": 3},
]

for city in cities:
    popup_html = f"<b>{city['name']}</b><br>Population: {city['population']} million"
    folium.Marker(
        location=[city["lat"], city["lon"]],
        popup=folium.Popup(popup_html, max_width=200),
        tooltip=city["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(markers_layer)
markers_layer.add_to(m)

Fullscreen().add_to(m)
folium.LayerControl().add_to(m)

m.save("bangladesh_folium project.html")