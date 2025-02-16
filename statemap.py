import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from dataAnalysis import AirbnbData
from streamlit_folium import folium_static

air = AirbnbData("Airbnb_Open_Data.csv")
air.preprocess()
air.entriesPerCounty("geoJsonData/new-york-counties.geojson")
df = air.getdf()

# Function to load geographical data and population data
def load_data():
    # Load a GeoJSON file with county boundaries (replace with your file)
    counties = gpd.read_file("geoJsonData/new-york-counties.geojson")
    # Add population data to the GeoDataFrame
    return counties

# Function to create a Folium map with a heatmap overlay
def create_heatmap(counties):
    # Create a Folium map centered on New York
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

    # Add the choropleth layer (heatmap)


    folium.GeoJson(
    counties,  # GeoJSON data
    name="New York Counties",  # Layer name
    style_function=lambda feature: {
        "fillColor": "white",  # Fill color for counties
        "color": "black",  # Border color
        "weight": 1,  # Border width
        "fillOpacity": 0,  # Fill opacity
    },
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["County:"])  # Tooltip for counties
    ).add_to(m)
    heatVal = 20
    HeatMap(data=df[['lat', 'long', "Construction year"]].values.tolist(), radius=12).add_to(m)

    return m

# Streamlit app
def main():
    st.title("Population Heatmap by County")

    # Load the data
    counties = load_data()

    # Create the heatmap
    st.write("Generating heatmap...")
    heatmap = create_heatmap(counties)

    # Display the map in Streamlit
    folium_static(heatmap, width = 725)

if __name__ == "__main__":
    main()