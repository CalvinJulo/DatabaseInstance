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


st.write('### The head documents')
st.dataframe(docs_df.head())
st.write('### The documents structure')
st.dataframe(docs_des)


# Add, Delete, Renew
st.write('### Add, Delete, Renew Documents')

original_df= docs_df
edited_df = st.data_editor(original_df, num_rows="dynamic")

if st.button("Save Changes"):
    # delete document
    original_ids = original_df["_id"].dropna().astype(str)
    original_ids = set(original_ids)
    edited_ids = set(edited_df["_id"].dropna())
    deleted_ids = original_ids - edited_ids
    # st.write('original_ids')
    # st.write(original_ids)
    st.write('edited_ids')
    st.write(edited_ids)
    st.write('deleted_ids')
    st.write(deleted_ids)
    for del_id in deleted_ids:
        col.delete_one({"_id": ObjectId(del_id)})
        st.write(del_id)

    # add new document
    new_rows = edited_df[edited_df["_id"].isna() | (edited_df["_id"] == "")]
    for idx, row in new_rows.iterrows():
        new_doc = row.to_dict()
        new_doc.pop("_id", None)
        st.write('new_doc')
        st.write(new_doc)
        if any(new_doc.values()):
            col.insert_one(new_doc)
            pass
    # renew document
    common_ids = original_ids.intersection(edited_ids)
    st.write('common_ids')
    st.write(common_ids)
    for row_id in common_ids:
        original_row = original_df[original_df["_id"] == ObjectId(row_id)].iloc[0].to_dict()
        edited_row = edited_df[edited_df["_id"] == row_id].iloc[0].to_dict()
        original_row.pop("_id", None)
        edited_row.pop("_id", None)
        if original_row != edited_row:
            col.update_one({"_id": ObjectId(row_id)}, {"$set": edited_row})
            st.write('edited_row')
            st.write(edited_row)
    st.write('Change saved')
    



st.write('###  Data Store from MongoDB')

tab1_1, tab1_2 = st.tabs(["Download", "Upload"])

with tab1_1:
    # Download data from MongoDB
    st.write('Download data from MongoDB')
    if docs:
        docs_to_json = dumps(docs)
        st.write(docs_to_json)
        st.download_button(
            label="Download MongoDB Data as JSON",
            data=docs_to_json,
            file_name="mongodb_data.json",
            mime="application/json")
    
with tab1_2:
    # upload data to MongoDB
    st.write('upload data to MongoDB')
    uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])
    if uploaded_file is not None:
        # Read file contents as a string
        file_contents = uploaded_file.getvalue().decode("utf-8")
        json_to_docs = loads(file_contents)
        if not isinstance(json_to_docs, list):
            json_to_docs = [json_to_docs]
        for doc in json_to_docs:
            if "_id" in doc:
                del doc["_id"]
        insert_docs = col.insert_many(json_to_docs)
        st.success(f"Inserted {len(insert_docs.inserted_ids)} documents into MongoDB.")



st.write('***')

# edit client, database, collection

st.write('### edit client, database, collection')

tab2_1, tab2_2, tab2_3 = st.tabs(["Client", "DB", "Col"])

with tab2_1:
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
with tab2_2:
    st.write(db.name)
    # st.write(db.watch())
    # db_stats = db.command("dbStats")
    # st.write(db_stats)
    st.write(db.list_collection_names())
    new_col_name = st.text_input("Add a new collection name")
    if new_col_name:
        new_col = db.create_collection(new_col_name)
        new_col.insert_one({"message": "Hello, MongoDB!"})
        st.write(db.list_collection_names())
    drop_col= st.text_input("Drop a collection")
    if drop_col:
        db[drop_col].drop()

with tab2_3:
    st.write(col.full_name)
    st.write(col.name)
    # col_stats = db.command("collStats", col.name)
    # st.write(col_stats)
    rename_col= st.text_input("Rename a collection")
    if rename_col:
        col.rename(rename_col)
    
