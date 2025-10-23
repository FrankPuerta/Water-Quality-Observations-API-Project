import pandas as pd
import streamlit as st
import plotly.express as px
import requests

baseurl = "http://localhost:5000"

st.set_page_config(page_title="Dashboard",
                   layout="wide")
st.title("🌊 Water Quality Dashboard 🌊")
st.header("CIS 3590 - Internship Ready Software Development")
st.subheader("Frank, Chris, Mari, Oscar, Gabriel")

st.write("Total Docs in DB:" + str(requests.get(f"{baseurl}/api/stats").json()))


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

# --------------------------------------
st.sidebar.divider()
st.sidebar.subheader("Min/Max Filters")

# --------------------------------------
st.sidebar.divider()
st.sidebar.subheader("Limit and Pagination")
limit = st.sidebar.number_input("Limit", min_value=100, max_value=1000, value=100)
page = st.sidebar.number_input("Page", min_value=1, max_value=10, value=1)

# --------------------------------------
st.sidebar.divider()
left_button, right_button = st.sidebar.columns(2)
if left_button.button("Pull Data", width="stretch"):
    left_button.success("Filter Applied")
if right_button.button("API Health", type="secondary", width="stretch"):
    response = requests.get(f"{baseurl}/api/health")
    if response.status_code == 200:
        right_button.success("API is Healthy!")
    else:
        right_button.error("API is Down!")

# """
# --------------------------------------
# -           Main Page                -
# --------------------------------------
# """
st.divider()

lineChart, histogram, scatterPlot, maps = st.tabs(["Line Chart", "Histogram", "Scatter Plot", "Maps"])

with lineChart:
    st.write("Line Chart")
    
with histogram:
    st.write("Histogram")
    
with scatterPlot:
    st.write("Scatter Plot")
    
with maps:
    st.write("Maps")
    

# """
# --------------------------------------
# -          Stats Panel               -
# --------------------------------------
# """
st.divider()
st.subheader("Statistics Panel")
stat = st.selectbox("Select Statistic", options=["Temperature (c)", "Salinity (ppt)", "pH", "Turbid+ NTU", "Chl ug/L", "BGA-PC cells/mL", "ODOsat %", "ODO mg/L"])

if st.button("Get Stats"):
    st.write(f"Fetching stats for: {stat}")
    # st.write(f"{baseurl}/api/stats?stat={stat}") debugging
    st.table(requests.get(f"{baseurl}/api/stats?field={stat}").json())