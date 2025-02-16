import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
import json
# Sample data: Replace this with your actual data
data = {
    'latitude': [40.7128, 40.7306, 40.7392, 40.7488, 40.7589],
    'longitude': [-74.0060, -73.9352, -73.9928, -73.9857, -73.9851],
    'weight': [10, 20, 30, 40, 50]  # Weight for heatmap intensity
}

if "clicked_county" not in st.session_state:
    st.session_state.clicked_county = None

# Convert data to a DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.title("New York City Heatmap")

with open("geoJsonData/new-york-counties.geojson") as f:
    NYcounties = json.load(f)

Max_Bounds = [[40.4774, -74.2591], [40.9176, -73.7004]]

#[42.6012, -76.1805]
m = folium.Map( location = [42.6012, -76.1805], 
                zoom_start = 6, 
                min_zoom = 6, 
                max_zoom = 18, 
                control_scale = True,
                #bounds = Max_Bounds
)

folium.GeoJson(
    NYcounties,  # GeoJSON data
    name="New York Counties",  # Layer name
    style_function=lambda feature: {
        "fillColor": "white",  # Fill color for counties
        "color": "black",  # Border color
        "weight": 1,  # Border width
        "fillOpacity": 0.2,  # Fill opacity
    },
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["County:"])  # Tooltip for counties
).add_to(m)

# Add a heatmap layer to the map
HeatMap(data=df[['latitude', 'longitude', 'weight']].values.tolist(), radius=15).add_to(m)

click_js = """
<script>
// Add a click event listener to the map
const map = window.map;
map.on('click', function(e) {
    console.log("womp");
    // Get the latitude and longitude of the click
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // Send a POST request to the server
    fetch('/handle_click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ lat: lat, lng: lng })
    })
    .then(response => response.json())
    .then(data => {
        // Display the server's response
        alert(data.message || data.error);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred.');
    });
});
</script>
"""

# Display the map in Streamlit
st.components.v1.html(m._repr_html_() + click_js, width=700, height=500)

if st.session_state.clicked_county:
    st.write(f"Clicked County: {st.session_state.clicked_county}")
