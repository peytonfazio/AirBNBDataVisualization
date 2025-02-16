import plotly.express as px
import pandas as pd
from dataAnalysis import AirbnbData
import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("airbnb_style.css")

air = AirbnbData("Airbnb_Open_Data.csv")
air.preprocess()
air.entriesPerCounty("new-york-counties.geojson")
df = air.getdf()

left, right = st.columns(2, gap="large")


# Function to load geographical data and population data
def load_data():
    # Load a GeoJSON file with county boundaries (replace with your file)
    counties = gpd.read_file("geoJsonData/new-york-counties.geojson")
    # Add population data to the GeoDataFrame
    return counties

# Logo

st.sidebar.image("air-o-lyze-logo.png")



fields = ['lat', 'long', 'Construction year', 'price', 'service fee', 'minimum nights', 'reviews per month', 'availability 365']
mapField = ['Construction year', 'price', 'service fee', 'minimum nights', 'reviews per month', 'availability 365']

mapWeight = st.sidebar.selectbox(
        "Select a field for the heatmap to use as a weight: ",
        mapField,
        )


# Function to create a Folium map with a heatmap overlay
def create_heatmap(counties):
    # Create a Folium map centered on New York
    m = folium.Map(
            location=[40.7128, -74.0060], 
            zoom_start=10,
            zoom_control=False,
            dragging=False,
        )

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
    
    heat_data = df[['lat', 'long', mapWeight]].values.tolist()
    HeatMap(data=heat_data, radius=12).add_to(m)

    return m

with left:
    # Streamlit app
    st.title("Population Heatmap by County")

    # Load the data
    counties = load_data()

    # Create the heatmap
    st.write("Generating heatmap...")
    heatmap = create_heatmap(counties)

    # Display the map in Streamlit
    folium_static(heatmap, width = 625)


def IQRBounds(x, df):
    # Calculate IQR
    Q1 = df[x].quantile(0.25)
    Q3 = df[x].quantile(0.75)
    IQR = Q3 - Q1

    # Define outlier bounds
    lowerBound = Q1 - 1.5 * IQR
    upperBound = Q3 + 1.5 * IQR

    return lowerBound, upperBound

with right:
    st.title("AirBNB Linear and Parallel Graph")


# County Fiddle
countySet = list(set(df["county"]))
countySet.remove(countySet[0])


county = st.sidebar.selectbox(
        "Select county to focus on:",
        countySet
        )

countyRows = df[df['county'] == county]

# Parallel Code
with right:
    nClusters = st.slider(
        "Number of Clusters:",  # Label for the slider
        min_value=1,  # Minimum value
        max_value=10,  # Maximum value
        value=4,  # Default value
        step=1  # Step size (optional)
    )

labels, centroids = air.cluster(nClusters, county)

centroiddf = countyRows
centroiddf['Cluster'] = [i for i in labels]

samplec = int(1000/nClusters)
if samplec > len(centroiddf.index):
    samplec = len(centroiddf.index)

centroiddfSamp = centroiddf.sample(n=samplec)
dims = ['lat', 'long', 'price', 'service fee', 'availability 365', 'reviews per month']

fig = px.parallel_coordinates(
        centroiddfSamp,
        dimensions = dims,
        color='Cluster',
        color_continuous_scale=px.colors.diverging.Tealrose,
)

with right:
    st.plotly_chart(fig)



# Graphing Code


#countySet.remove("nan")




horzDisplay = st.sidebar.selectbox(
    "Select field for horizontal axis to display:",
    fields,
    index=3
)


vertDisplay = st.sidebar.selectbox(
    "Select field for vertical axis to display:",
    fields,
    index=5
)

with right:
    sample = st.slider(
    "Sample Size:",  # Label for the slider
    min_value=1,  # Minimum value
    max_value= min(len(countyRows), 500),  # Maximum value
    value=min(len(countyRows), 50),  # Default value
    step=1  # Step size (optional)
)

    st.write(county + " has " + str(len(countyRows)) + " rows")
dfcountysample = countyRows.sample(n=sample, random_state=42)


lower_bound, upper_bound = IQRBounds(horzDisplay, dfcountysample)
bounddf= dfcountysample[(dfcountysample[horzDisplay] >= lower_bound) & (df[horzDisplay] <= upper_bound)]


lineFig = px.scatter(
    bounddf,
    x=horzDisplay,
    y=vertDisplay,
    render_mode='svg'
)

# Line Chart Graph
with right:
    st.header("Line Chart (" + horzDisplay + ", " + vertDisplay + ")")
    rsquare = air.rSquared(horzDisplay, vertDisplay)
    st.write("R Squared: " + str(rsquare))
    if rsquare < 0.5:
        st.write("No correlation")
    else:
        st.write("Some correlation")

    st.plotly_chart(lineFig)
    #st.line_chart(data=dfpercent, x=horzDisplay, y=vertDisplay, use_container_width=True)

#with col2:
#    st.write("r squared " + rSquared(horzDisplay, vertDisplay))


st.sidebar.text("Air-o-lyze is a data analysis tool for deriving insights from Airbnb data.\nView groupings of rentals using the heatmap overlay.\nIdentify clusters of data and the particular trends within each cluster using the parallel coordinates chart on the right.\nBelow the parallel coordinates chart, you can find an adjustable linear regression chart. Select the axes using the drop-down menus on the left hand side.")
