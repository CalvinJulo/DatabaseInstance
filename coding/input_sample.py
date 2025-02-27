# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description：
"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def get_mongodb(username, password):
    # Create a new client and connect to the server
    # Initialize connection.
    uri = f"mongodb+srv://{username}:{password}@cluster0.v53a0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        ping = "Pinged your deployment. You successfully connected to MongoDB!"
        print(ping)
    except Exception as e:
        print(e)
    return client


