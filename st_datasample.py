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
from bson import ObjectId


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
def get_docs_df_des(df):
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
docs = get_col(db_name, col_name)
docs_df = pd.DataFrame(docs)

# Show the example of documents
st.write('### The head documents')
st.dataframe(docs_df.head())

# Show the structure of documents
st.write('### The documents structure')
des = get_docs_df_des(docs_df)
st.dataframe(des)


# Show the Document field
st.write('### The field of Documents')
keys = set(key for dict_ in docs for key in dict_.keys())
st.write(list(keys))

# Show the field value
st.write('### The value of Field')
value_name = st.text_input('value_name')
values = []
for i in docs:
    values.append(i[value_name])
st.dataframe(values)




# Add, Delete, Renew
original_df= docs_df
edited_df = st.data_editor(original_df, num_rows="dynamic")

if st.button("Save Changes"):
    # delete document
    original_ids = set(original_df["_id"].dropna())
    edited_ids = set(edited_df["_id"].dropna())
    deleted_ids = original_ids - edited_ids
    for del_id in deleted_ids:
        col.delete_one({"_id": ObjectId(del_id)})

    # add new document
    new_rows = edited_df[edited_df["_id"].isna() | (edited_df["_id"] == "")]
    for idx, row in new_rows.iterrows():
        new_doc = row.to_dict()
        new_doc.pop("_id", None)
        if any(new_doc.values()):
            col.insert_one(new_doc)
    st.write('Change saved')

















# Update the docs
# unsoloved problem,1, guarentee the type of value; 2, only update changed docs
# Display the DataFrame in a data editor for user editing
edited_docs_df = st.data_editor(docs_df, num_rows="dynamic")

# Button to trigger the update process
# check every docs in edited_df, and use _id to update the whole doc
if st.button("Update Database"):
    # Iterate over rows in the edited DataFrame
    for index, row in edited_docs_df.iterrows():
        # Get the document _id and convert it back to an ObjectId
        doc_id = ObjectId(row["_id"])

        # Prepare the update data (exclude the _id field)
        update_doc = row.to_dict()
        update_doc.pop("_id", None)
        # Update the document in MongoDB
        col_update_one = col.update_one({"_id": doc_id}, {"$set": update_doc})
        st.write(f"Row {index} updated; modified count: {col_update_one.modified_count}")




# edit client, database, collection

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

with tab3:
    st.write(col.full_name)
    st.write(col.name)
    # col_stats = db.command("collStats", col.name)
    # st.write(col_stats)
    rename_col= st.text_input("Rename a collection")
    if rename_col:
        col.rename(rename_col)
    
