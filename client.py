import pandas as pd
import streamlit as st
import plotly.express as px
import requests

base_url = "http://127.0.0.1:5000"

st.title("Water Quality Observations")

tab1, tab2= st.tabs([
    "Tab 1",
    "Tab 2"
])

with tab1:
    st.write("First tab")
    if st.button("Water Quality Observations Data Columns"):
        response = requests.get(base_url + "/data").json()
        st.dataframe(pd.DataFrame(response))