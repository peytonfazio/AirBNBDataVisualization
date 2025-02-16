import streamlit as st
import plotly.express as px
import pandas as pd
from dataAnalysis import AirbnbData

def IQRBounds(x, df):
    # Calculate IQR
    Q1 = df[x].quantile(0.25)
    Q3 = df[x].quantile(0.75)
    IQR = Q3 - Q1

    # Define outlier bounds
    lowerBound = Q1 - 1.5 * IQR
    upperBound = Q3 + 1.5 * IQR

    return lowerBound, upperBound


st.title("AirBNB Linear and Parallel Graph")
air = AirbnbData("Airbnb_Open_Data.csv")
air.preprocess()
air.entriesPerCounty("new-york-counties.geojson")
df = air.getdf()

# County Fiddle
countySet = list(set(df["county"]))
county = st.sidebar.selectbox(
    "Select county to focus on:",
    countySet
)

countyRows = df[df['county'] == county]

# Parallel Code

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

st.plotly_chart(fig)



# Graphing Code


#countySet.remove("nan")

fields = ['lat', 'long', 'Construction year', 'price', 'service fee', 'minimum nights', 'reviews per month', 'availability 365']

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

# Parallel coordinates graph
#st.header("Parallel Coordinates")
#fig = px.parallel_coordinates(
#    df,
#    dimensions=df.columns,  # Columns
#    color='price',  # Color by Column
#    color_continuous_scale=px.colors.diverging.Tealrose,  # Color scale
#    labels={'price': 'price', 'bedrooms' : 'bedrooms', 'availability' : 'availability'}
#)

#st.plotly_chart(fig)

# Line Chart Graph

with st.container():
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

