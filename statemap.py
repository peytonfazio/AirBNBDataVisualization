import streamlit as st
import geopandas as gpd
import folium
import requests
from streamlit_folium import folium_static

# Function to load geographical data and population data
def load_data():
    # Load a GeoJSON file with county boundaries (replace with your file)
    counties = gpd.read_file("geoJsonData/new-york-counties.geojson")

    # Example population data (replace with your data)
    population_data = {
        "New York County, New York": 1664727,
        "Kings County, New York": 2648452,
        "Queens County, New York": 2405464,
        "Bronx County, New York": 1471160,
        "Richmond County, New York": 495747,
        # Add more counties and population data as needed
    }

    # Add population data to the GeoDataFrame
    counties["population"] = counties["name"].map(population_data)

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

    return m

def checkClicks(clickTest):
    click_data = st.session_state.get("click_data", None)
    if click_data:
        st.write(f"Clicked at: {click_data}")

        # Send the click data to the Flask backend
        response = requests.post("http://localhost:5000/process_click", json=click_data)
        if response.status_code == 200:
            st.write("Backend response:", response.json())
        else:
            st.write("Failed to send data to the backend.")
    if clickTest:
        if st.button("Simulate Click"):
            st.session_state["click_data"] = {"lat": 40.7128, "lon": -74.0060}  # Example: NYC coordinates


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

    checkClicks(True)

if __name__ == "__main__":
    main()