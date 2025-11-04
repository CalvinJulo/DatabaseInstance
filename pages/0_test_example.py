# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：
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
import json
import plotly.express as px

st.info('This is the basic intro of mongodb\n\n-- connect to Mongodb Altas\n\n-- CRUD DB, Col, Doc')


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
@st.cache_data(ttl=600)
def get_col(db, col):
    documents = client[db][col].find()
    documents = list(documents) # make hashable for st.cache_data
    return documents


# Show the Database and its Collection from the MongoDB
client = get_mongo()
with st.sidebar:
    db_name_list = [name for name in client.list_database_names() if name not in ['admin', 'config', 'local']]
    db_name = st.selectbox('Database', db_name_list)
    col_name = st.selectbox('Collection', client[db_name].list_collection_names())
    st.write('current_db:', db_name)
    st.write('current_col:', col_name)


# Show the collection info in DataFrame
st.write('##', db_name, col_name)
db = client[db_name]
col = db[col_name]
docs = get_col(db_name, col_name) # docs is a list of documents, and documents is a dict or json
docs_df = pd.DataFrame(docs)
docs_jn_df =pd.json_normalize(docs,sep='.')
docs_des = run_mongo.get_docs_df_des(docs_jn_df)
docs_fields = set(key for dict_ in docs for key in dict_.keys())


st.write('### The head documents')
st.dataframe(docs_df.head())
st.write('### The documents structure')
st.dataframe(docs_des)
st.write('### The documents description')
st.dataframe(docs_jn_df.describe(include='all').T)
select_field = st.pills('field',docs_jn_df.columns.tolist(),selection_mode="multi",default=None)

if len(select_field)==1:
    fig = px.histogram(docs_jn_df, x=select_field, marginal="box", title=f'Distribution of {select_field}')
    st.plotly_chart(fig, use_container_width=True)
elif len(select_field)==2:
    fig = px.scatter(docs_jn_df, x=select_field[0], y=select_field[1], title=f'{select_field[0]} vs. {select_field[1]}')
    st.plotly_chart(fig, use_container_width=True)
elif len(select_field)>2:
    fig = px.scatter_matrix(docs_jn_df,dimensions=select_field,title="Multivariate Relationships")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write('reselect')

# Filter
st.write('### Filter, Search Documents')



st.text("example: [{'$match': {'rated': 'TV-G'}},{'$match': {'runtime': {'$gt': 1}}},{'$match': {'name': {'$regex':'Ned','$options':'i'}}]")


condition = st.text_input("condition",'[]')

pipeline=json.loads(condition.replace("'", '"'))
#pipeline=[].append({'$match': {'rated': 'TV-G'}})

filter_result = col.aggregate(pipeline)
st.write(pd.json_normalize(list(filter_result),sep='.'))

# st.write(pd.json_normalize(find_docs_result,record_path='nested_list_field',sep='_',errors='ignore'))
#st.write(pd.DataFrame(find_docs_result))




# Add, Delete, Renew
st.write('### Add, Delete, Renew Documents')

original_df= docs_df
edited_df = st.data_editor(original_df, num_rows="dynamic")



if st.button("Save Changes"):
    original_ids = original_df["_id"].dropna().astype(str)
    original_ids = set(original_ids)
    edited_ids = set(edited_df["_id"].dropna())
    deleted_ids = original_ids - edited_ids
    common_ids = original_ids.intersection(edited_ids)
    st.write('delete document') # delete document
    for del_id in deleted_ids:
        col.delete_one({"_id": ObjectId(del_id)})
        st.write(del_id)

    st.write('Add document') # add new document
    new_rows = edited_df[edited_df["_id"].isna() | (edited_df["_id"] == "")]
    for idx, row in new_rows.iterrows():
        new_doc = row.to_dict()
        new_doc.pop("_id", None)
        st.write(new_doc)
        if any(new_doc.values()):
            col.insert_one(new_doc)
            pass
    st.write('Renew document')# renew document
    for row_id in common_ids:
        original_row = original_df[original_df["_id"] == ObjectId(row_id)].iloc[0].to_dict()
        edited_row = edited_df[edited_df["_id"] == row_id].iloc[0].to_dict()
        original_row.pop("_id", None)
        edited_row.pop("_id", None)
        if original_row != edited_row:
            col.update_one({"_id": ObjectId(row_id)}, {"$set": edited_row})
            st.write(edited_row)
    st.write('Change saved')
    



st.write('###  Data Store from MongoDB')

tab1_1, tab1_2 = st.tabs(["Download", "Upload"])

with tab1_2:
    # Download data from MongoDB
    st.write('Download data from MongoDB')
    if docs:
        docs_to_json = dumps(docs)
        # st.write(docs_to_json)
        st.download_button(
            label="Download MongoDB Data as JSON",
            data=docs_to_json,
            file_name="mongodb_data.json",
            mime="application/json")
    
with tab1_1:
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

'''
structure_list=[]
for i in client.list_database_names():
    structure_db = client[i]
    for j in client[i].list_collection_names():
        structure_dict={}
        structure_dict['db']=i
        structure_dict['col']=j
        structure_dict['docs_num']=structure_db[j].estimated_document_count()
        # structure_stats = structure_db.command('collstats', j)
        # structure_dict['col_size']= round(structure_stats.get('size', 0) / (1024 * 1024), 2) # size 是集合的逻辑大小（字节），除以 1024^2 转换为 MB
        structure_dict['col_size']=''
        structure_dict['docs_field'] = set(key for dict_ in get_col(i, j)  for key in dict_.keys())
        structure_list.append(structure_dict)
st.write(pd.DataFrame(structure_list))
'''





tab2_1, tab2_2, tab2_3, tab2_4 = st.tabs(["Client", "DB", "Col","Doc"])

with tab2_1:
    # st.write(client.server_info())
    # st.write(client.watch())
    st.write('database list in Client')
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
    st.write('collection list in',db.name)
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
    st.write('Current collection:',col.full_name)
    st.write(col.name)
    # col_stats = db.command("collStats", col.name)
    # st.write(col_stats)
    rename_col= st.text_input("Rename the collection")
    if rename_col:
        col.rename(rename_col)
    
with tab2_4:
    st.write('fields in',col.full_name)
    st.write(docs_fields)
    old_field = st.text_input("Old Field Name", key="rename_old")
    new_field = st.text_input("New Field Name", key="rename_new")
    if st.button('Rename field'):
        if old_field and new_field:
            rename_res = col.update_many({}, {"$rename": {old_field: new_field}})
            st.success(f"Renamed field '{old_field}' to '{new_field}' in {rename_res.modified_count} document(s).")
    added_field_name = st.text_input("Add new Field Name", key="add_field")
    if st.button("Add New Field"):
        if added_field_name:
            added_res = col.update_many({}, {"$set": {added_field_name: None}})
            st.success(f"Added field '{added_field_name}' with default value 'None' to {added_res.modified_count} document(s).")
 
    

