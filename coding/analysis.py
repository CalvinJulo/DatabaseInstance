# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description：
"""

import pandas as pd


# show the description of df
def df_des(df):
    des = pd.DataFrame()
    for i in df.columns:
        name_dict = dict()
        name_dict['name'] = i
        name_dict['type'] = df[i].dtype
        name_dict['example'] = df[i][0]
        name_dict['num'] = df[i].count()
        des = des.append(name_dict, ignore_index=True)
    return des



