# coding=utf-8

import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

with st.sidebar:
    if st.button('Altas'):
        Username = st.text_input('Username','calvinish')
        Password = st.text_input('password','kKS8NAQmdgSqT1c8')
    uri = f"mongodb+srv://{Username}:{Password}@cluster0.f8fu9.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return MongoClient(uri, server_api=ServerApi('1'))

client = init_connection()

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    st.write("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.write(e)

with st.sidebar:
    db = st.selectbox('Database', client.list_database_names())
    st.write(db.list_collection_names())
