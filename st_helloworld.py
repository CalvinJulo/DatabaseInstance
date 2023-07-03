# coding=utf-8

import streamlit as st
import pymongo

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb+srv://zcglook:OINbHLNnoSuvCjnud@cluster0.lfgvy2a.mongodb.net/?retryWrites=true&w=majority")
st.write('OK')
client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()

st.write(items)
