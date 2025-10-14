import pandas as pd
import streamlit as st
import plotly.express as px
import requests

st.set_page_config(page_title="Dashboard",
                   layout="wide")
st.title("🌊 Water Quality Dashboard 🌊")
st.header("CIS 3590 - Internship Ready Software Development")
st.subheader("Frank, Chris, Mari, Oscar, Gabriel")


# """
# --------------------------------------
# -           Sidebar Stuff            -
# --------------------------------------
# """
st.sidebar.title("Control Panel")
st.sidebar.divider()

start_date, end_date = st.sidebar.select_slider(
        "Date Range",
        options = ["10/16/2021", "12/16/2021", "10/07/2022", "11/16/2022"], 
        value = ("10/16/2021","11/16/2022")
    )

st.sidebar.divider()

# """
# --------------------------------------
# -           Main Page                -
# --------------------------------------
# """
st.divider()
df = pd.read_csv("cleaned_datasets/2021-dec16.csv")

lineChart, histogram, scatterPlot, maps = st.tabs(["Line Chart", "Histogram", "Scatter Plot", "Maps"])

with lineChart:
    st.write("Line Chart")
    
with histogram:
    st.write("Histogram")
    
with scatterPlot:
    st.write("Scatter Plot")
    
with maps:
    st.write("Maps")
    