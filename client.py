import pandas as pd
import streamlit as st
import plotly.express as px
import requests

baseurl = "http://localhost:5000"

st.set_page_config(page_title="Dashboard",
                   layout="wide")
st.title("🌊 Water Quality Dashboard 🌊")
st.header("CIS 3590 - Internship Ready Software Development")

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
        options = ["10/21/2021", "12/16/2021", "10/07/2022", "11/16/2022"], 
        value = ("10/21/2021","11/16/2022")
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


# """
# --------------------------------------
# -           Data table               -
# --------------------------------------
# """

# ---- UI state ----
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None
if "api_url" not in st.session_state:
    st.session_state.api_url = ""

st.divider()
st.subheader("Data Table")

refresh = st.button("🔄Refresh Data",  type="primary")

if refresh:
    try:
        with st.spinner("Fetching data..."):
            observations_url = f"/api/observations?start={start_date}&end={end_date}&temp_min={temp_min}&temp_max={temp_max}&sal_min={sal_min}&sal_max={sal_max}&odo_min={odo_min}&odo_max={odo_max}&limit={limit}&page={page}"
            observations_dataSet = requests.get(f"{baseurl}{observations_url}").json()
            observations_df = pd.DataFrame(observations_dataSet["items"])

        st.session_state.df = observations_df
        st.session_state.api_url = observations_url
        st.success("Data refreshed!")
    except requests.HTTPError as e:
        st.error(f"HTTP error: {e}")
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
    except ValueError as e:
        st.error(f"Data parsing failed: {e}")

st.dataframe(st.session_state.df, use_container_width=True, key="main_df")
# """
# --------------------------------------
# -           Visualizations           -
# --------------------------------------
# """
st.divider()
st.subheader("Visualizations Panel")
date = st.segmented_control(label="Select Date Field", options=["10/21/2021", "12/16/2021", "10/07/2022", "11/16/2022"] , key="linechart_date") 
if date == None:
    date = "10/16/2021"
st.write(f"Selected Date: {date}")
lineChart, histogram, scatterPlot, maps = st.tabs(["Line Chart", "Histogram", "Scatter Plot", "Maps"])

linechart_url = f"{baseurl}/api/lineChart?date={date}"
linechart_dataSet = requests.get(linechart_url).json()
df = pd.DataFrame(linechart_dataSet["data"])


with lineChart:
    st.write("Line Chart")

    min_time, max_time = st.slider(
        "Time Range",
        min_value=0,
        max_value=len(df),
        value=(50, 250),
        step=5
    )

    linechart_df = df.iloc[int(min_time):int(max_time)]
    # st.write(linechart_df.columns)
    st.line_chart(linechart_df[["pH","Temperature (c)", "Salinity (ppt)", "ODO mg/L", "Time"]], x="Time", y=["pH","Temperature (c)", "Salinity (ppt)", "ODO mg/L"], width='stretch')
    # st.line_chart(linechart_df[["Temperature (c)", "Salinity (ppt)", "ODO mg/L"]], x="Time", y=["Temperature (c)", "Salinity (ppt)", "ODO mg/L"], width='stretch')
    # st.line_chart(observations_df[["Temperature (c)", "Salinity (ppt)", "ODO mg/L"]], x_label="Index", y_label="Values", width='stretch')
    
with histogram:
    st.write("Histogram")


    st.bar_chart(df, y="Temperature (c)", x="Salinity (ppt)")

with scatterPlot:
    st.write("Scatter Plot")

    fig = px.scatter(df, x="Salinity (ppt)", y="Temperature (c)", color="ODO mg/L")
    st.plotly_chart(fig)
    
with maps:
    st.write("Maps")

    figMap = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="pH", hover_data=df, zoom=17, mapbox_style="open-street-map")
    st.plotly_chart(figMap)

# IF WE WANT ANY MORE VISUALIZATIONS, WE CAN ADD THEM HERE.
    

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

st.divider()

st.write("Created By:")
st.subheader("Gabriel")
