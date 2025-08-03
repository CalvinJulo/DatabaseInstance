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

st.info('This is analysis mode')
st.info('Get the sample of mongodb')
st.info('Show the structure of the sample data')
st.info('Search the sample data')
st.info('Visualize the outcome')



current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
st.write('Current time:',current_time)
