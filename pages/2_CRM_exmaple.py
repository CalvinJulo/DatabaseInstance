# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description：
"""
# CMD Run Command ： streamlit run /Users/xx.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pandas as pd
import streamlit as st
from bson import ObjectId
from bson.json_util import dumps,loads
from pages.common_lib import run_mongo
import time



current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
st.write('Current time:',current_time)

# Username and password from MongoDB Altas
with st.sidebar:
    Username = st.text_input('Username', 'mongo01')
    Password = st.text_input('password', 'k78Zcoy3CSxL3Dfo')

# Create a new client and connect to the server
# Initialize connection. And return the client
# And should ensure it only run once.
@st.cache_resource
def get_mongo():
    client = run_mongo.connect_mongo(Username, Password)
    return client

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_resource
def get_col(db, col):
    documents = client[db][col].find()
    documents = list(documents) # make hashable for st.cache_data
    return documents


# Show the Database and its Collection from the MongoDB
client = get_mongo()
with st.sidebar:
    db_name = st.selectbox('Database', client.list_database_names())
    col_name = st.selectbox('Collection', client[db_name].list_collection_names())
    st.write('current_db:', db_name)
    st.write('current_col:', col_name)


# Show the collection info in DataFrame
st.write('##', db_name, col_name)
db = client[db_name]
col = db[col_name]
docs = get_col(db_name, col_name) # docs is a list of documents, and documents is a dict or json
docs_df = pd.DataFrame(docs)
docs_des = run_mongo.get_docs_df_des(docs_df)
docs_fields = set(key for dict_ in docs for key in dict_.keys())

with st.sidebar:
    option = st.popover("Option")
    with option:
        if st.button("Initial"):
            intial_doc = {"name": 'name',"email": 'email',"phone": 'phone',"company": 'company',"notes": 'notes'}
            col.insert_one(intial_doc)
            st.success(f"Inital collection!")
    with option:
        st.write('sss')



st.write('### The head documents')
st.dataframe(docs_df.head())
st.write('### The documents structure')
st.dataframe(docs_des)


    


