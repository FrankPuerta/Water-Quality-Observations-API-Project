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

# st.write("Total Docs in DB:" + str(requests.get(f"{baseurl}/api/stats").json()))


# """
# --------------------------------------
# -           Sidebar Stuff            -
# --------------------------------------
# """
st.sidebar.title("Control Panel")
st.sidebar.divider()

# --------------------------------------
st.sidebar.subheader("Min/Max Filters")

start_date, end_date = st.sidebar.select_slider(
        "Date Range",
        options = ["10/16/2021", "12/16/2021", "10/07/2022", "11/16/2022"], 
        value = ("10/16/2021","11/16/2022")
    )

st.sidebar.subheader("Temperature Filter")
temp_min, temp_max = st.sidebar.slider(
        "Temperature (C) Range",
        min_value=25.0,
        max_value=33.0,
        value=(25.0, 33.0),
        step=0.5
    )

st.sidebar.subheader("Salinity Filter")
sal_min, sal_max = st.sidebar.slider(
        "Salinity (ppt) Range",
        min_value=0.0,
        max_value=50.0,
        value=(0.0, 50.0),
        step=0.5
    )

st.sidebar.subheader("ODO Filter")
odo_min, odo_max = st.sidebar.slider(
        "ODO mg/L Range",
        min_value=2.0,
        max_value=8.0,
        value=(2.0, 8.0),
        step=0.5
    )
# --------------------------------------
st.sidebar.divider()
st.sidebar.subheader("Limit and Pagination")
limit = st.sidebar.number_input("Limit", min_value=100, max_value=1000, value=100)
page = st.sidebar.number_input("Page", min_value=1, max_value=30, value=1)


# --------------------------------------
st.sidebar.divider()
left_button, right_button = st.sidebar.columns(2)
if left_button.button("Pull Data", width="stretch"):
    left_button.success("Filter Applied")
# if right_button.button("API Health", width="stretch"):
#     response = requests.get(f"{baseurl}/api/health")
#     if response.status_code == 200:
#         right_button.success("API is Healthy!")
#     else:
#         right_button.error("API is Down!")

# """
# --------------------------------------
# -           Data table               -
# --------------------------------------
# """

q_url = f"/api/observations?start={start_date}&end={end_date}&temp_min={temp_min}&temp_max={temp_max}&sal_min={sal_min}&sal_max={sal_max}&odo_min={odo_min}&odo_max={odo_max}&limit={limit}&page={page}"
dataSet = requests.get(f"{baseurl}{q_url}").json()

# MAIN DATAFRAME PULL FROM HERE vvvv-----------------
df = pd.DataFrame(dataSet["items"])

st.divider()
st.subheader("Data Table")

st.dataframe(df,width="stretch")


# """
# --------------------------------------
# -           Visualizations           -
# --------------------------------------
# """
st.divider()
st.subheader("Visualizations Panel")
lineChart, histogram, scatterPlot, maps = st.tabs(["Line Chart", "Histogram", "Scatter Plot", "Maps"])


with lineChart:
    st.write("Line Chart")
    st.line_chart(df[["Temperature (c)", "Salinity (ppt)", "ODO mg/L"]], x_label="Index", y_label="Values", use_container_width=True)
    
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
stats = st.multiselect("Select Statistic", options=["Temperature (c)", "Salinity (ppt)", "pH", "Turbid+ NTU", "Chl ug/L", "BGA-PC cells/mL", "ODOsat %", "ODO mg/L", "Conductivity (mmhos/cm)"])
api_call = None
if st.button("Get Stats"):
    st.write(f"Fetching stats for: {stats}")
    for stat in stats:
        if stat == "Turbid+ NTU":
            stat = "Turbid%2B%20NTU"
        api_call = f"{api_call}&field={stat}"

    # debugging ---
    # st.write(f"{baseurl}/api/stats?{api_call}") 

    st.table(requests.get(f"{baseurl}/api/stats?{api_call}").json())

# """
# --------------------------------------
# -          Outliers Panel            -
# --------------------------------------
# """

st.divider()
st.subheader("Outliers Panel")
