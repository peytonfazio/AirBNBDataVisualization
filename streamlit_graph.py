import streamlit as st
import plotly.express as px
import pandas as pd

st.title("AirBNB Linear and Parallel Graph")

# Test Database
data = {
    'price': [150, 200, 300, 120, 250],
    'bedrooms': [1, 2, 3, 1, 2],
    'availability': [30, 15, 10, 45, 20]
}

df = pd.DataFrame(data)

horzDisplay = st.sidebar.selectbox(
    "Select field for horizontal axis to display:",
    df.columns
)

vertDisplay = st.sidebar.selectbox(
    "Select field for vertical axis to display:",
    df.columns
)


# Parallel coordinates graph
st.header("Parallel Coordinates")
fig = px.parallel_coordinates(
    df,
    dimensions=df.columns,  # Columns
    color='price',  # Color by Column
    color_continuous_scale=px.colors.diverging.Tealrose,  # Color scale
    labels={'price': 'price', 'bedrooms' : 'bedrooms', 'availability' : 'availability'}
)

st.plotly_chart(fig)

# Line Chart Graph
st.header("Line Chart Graph (" + horzDisplay + ", " + vertDisplay + ")")
st.line_chart(data=df, x=horzDisplay, y=vertDisplay)

