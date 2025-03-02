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

import pandas as pd
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Username and password from MongoDB Altas
with st.sidebar:
    Username = st.text_input('Username', 'mongo01')
    Password = st.text_input('password', 'k78Zcoy3CSxL3Dfo')


st.write('hello, this is test')

# Create a new client and connect to the server
# Initialize connection. And return the client
# And should ensure it only run once.
@st.cache_resource
def get_mongo():
    uri = "mongodb+srv://mongo01:k78Zcoy3CSxL3Dfo@cluster0.v53a0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        st.write('Pinged your deployment. You successfully connected to MongoDB!')
    except Exception as e:
        print(e, 'Fail connect')
        st.write('Fail connect')
    return client


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_resource
def get_col(db, col):
    documents = client[db][col].find()
    documents = list(documents) # make hashable for st.cache_data
    return documents

# show the description of df of documents
def get_doc_df_des(df):
    des = []
    for i in df.columns:
        name_dict = dict()
        name_dict['field'] = i
        name_dict['type'] = df[i].dtype
        name_dict['value example'] = df[i][0]
        name_dict['num'] = df[i].count()
        des.append(name_dict)
    des = pd.DataFrame(des)
    return des

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
data = get_col(db_name, col_name)
df = pd.DataFrame(data)

# Show the example of documents
st.write('### The head documents')
st.dataframe(df.head())

# Show the structure of documents
st.write('### The documents structure')
des = get_doc_df_des(df)
st.dataframe(des)


# Show the Document field
st.write('### The field of Documents')
keys = set(key for dict_ in data for key in dict_.keys())
st.write(list(keys))

# Show the field value
st.write('### The value of Field')
value_name = st.text_input('value_name','')
values = []
for i in data:
    values.append(i[value_name])
st.dataframe(values)


tab1, tab2, tab3 = st.tabs(["Client", "DB", "Col"])

with tab1:
    # st.write(client.server_info())
    # st.write(client.watch())
    st.write(client.list_database_names())
    new_db_name = st.text_input("Add a new db name")
    if new_db_name:
        new_db = client[new_db_name] # Reference a new database (it will be created when data is inserted)
        new_col = new_db.create_collection('new collection')# Create a collection and insert a document to create the database
        st.write(client.list_database_names())
    drop_db = st.text_input("Drop a db")
    if drop_db:
        client.drop_database(drop_db)
with tab2:
    st.write(db.name)
    # st.write(db.watch())
    st.write(db.list_collection_names())
    new_col_name = st.text_input("Add a new collection name")
    if new_col_name:
        new_col = db.create_collection(new_col_name)
        st.write(db.list_collection_names())
    drop_col= st.text_input("Drop a collection")
    if drop_col:
        db[drop_col].drop()

