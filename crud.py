from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")

def get_connection(db_name):
    return myclient[db_name]

def insert_row(db_name,collection_name,json_obj):
    con = get_connection(db_name)
    collection = con[collection_name]
    collection.insert_one(json_obj)