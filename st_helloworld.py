# coding=utf-8

import streamlit as st
import pandas as pd

st.write('Hello World')

st.success('Welcome to Streamlit')

st.title("My Streamlit App")

# Load data
data_url = "https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/uber-raw-data-SEP14.csv.gz"
data = pd.read_csv(data_url, compression="gzip")

# Show data
st.write(data)
