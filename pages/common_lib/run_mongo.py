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

# Create a new client and connect to the server
# Initialize connection. And return the client
# And should ensure it only run once, use @st.cache_resource.
def connect_mongo(Username, Password):
    uri = f"mongodb+srv://{Username}:{Password}@cluster0.v53a0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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



# get the descrption of documents dataframe
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




