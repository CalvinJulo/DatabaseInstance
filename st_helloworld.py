# coding=utf-8

import streamlit as st
import pymongo
st.write('Start')
pymongo.MongoClient("mongodb+srv://zcglook:OINbHLNnoSuvCjnud@cluster0.lfgvy2a.mongodb.net/?retryWrites=true&w=majority")
st.write('Entry')
try:
    client.admin.command('ping')
    st.write("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.write(e)

st.write('End')
