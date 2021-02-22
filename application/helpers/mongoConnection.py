from pymongo import MongoClient

client = MongoClient()
db = client.Whatsapp.Users

def read_coll(collection,query,db=db,project=None):
    res = db[collection].find(query,project)
    return list(res)

def read(query, project=None):

    data = db.find(query, project)
    return list(data)

def write_coll(collection, obj,client=client):
    res = db[collection].insert_one(obj)
    return res

def update_coll(collection, query, update,client=client):
    setting = {"$set":update}
    res = db[collection].update_one(query,setting)
    return res

def delete_coll(collection, query, client=client):
    res = db[collection].delete_one(query)
    return res

def push_coll(collection, query, update,client=client):
    setting = {"$push":update}
    res = db[collection].update_one(query,setting)
    return res