import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import json

def obj_to_str(data):
    if isinstance(data, dict):
        return {obj_to_str(key): obj_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [obj_to_str(element) for element in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

user = "nepoun"
password = "qmRQVnB5Kz3FB6Mw"

client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@cluster1.xp7hqgb.mongodb.net/?retryWrites=true&w=majority")
db = client.vaultt

global mydb
mydb = client.vaultt

def convert_to_json(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

def getCol(db, escolha):
    mycol = db["users"]
    if(escolha == "1" or escolha == 1):
        mycol = db["users"]
    elif(escolha == "2"  or escolha == 2):
        mycol = db["games"]
    elif(escolha == "3"  or escolha == 3):
        mycol = db["directs"]
    elif(escolha == "4"  or escolha == 4):
        mycol = db["reviews"]
    return mycol


def insert(escolha, dict):
    #Insert
    global mydb
    mycol = getCol(mydb, escolha)
    x = mycol.insert_one(dict)
    return x


def findSort(escolha, field):
    #Sort
    global mydb
    mycol = getCol(mydb, escolha)
    mydoc = mycol.find().sort(field)
    for x in mydoc:
        return x

def findQuery(escolha, coluna, procura):
    #Query
    global mydb
    mycol = getCol(mydb, escolha)
    myquery = { coluna: procura }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        return x

def findMultipleQuery(escolha, coluna, procura):
    #Query
    global mydb
    mycol = getCol(mydb, escolha)
    myquery = { coluna: procura }
    mydoc = mycol.find(myquery)
    result = {}
    for x in mydoc:
        serialized_doc = json.loads(json.dumps(x, default=convert_to_json))
        result[str(x["_id"])] = serialized_doc
    return result
        

def findAll(escolha):
    global mydb
    print(f'\n\n {str(escolha)}')
    mycol = getCol(mydb, escolha)
    mydoc = mycol.find()
    result = {}
    for x in mydoc:
        serialized_doc = json.loads(json.dumps(x, default=convert_to_json))
        result[str(x["_id"])] = serialized_doc
    return result

def updateQuery(escolha, id, data):
    global mydb
    mycol = getCol(mydb, escolha)
    mycol.update_one({"_id": ObjectId(id)}, {"$set": data})

def pushNewMessage(idConversa, data):
    global mydb
    mycol = getCol(mydb, "3")
    mycol.update_one({"_id": ObjectId(idConversa)}, {"$push": { 'message': data }})

def addNewFriend(userId, friendId, username, friendName):

    try:  
        global mydb
        mycol = getCol(mydb, 1)

        directObject = {
            "TABLE_ID": 3,
            "message": {}
        }
        del directObject['TABLE_ID']
        directId = insert('3', obj_to_str(directObject)).inserted_id
        print(f"\n\n\n\n {directId}:: {type(directId)}")
        mycol.update_one({"_id": ObjectId(userId)}, {"$push": { "friends": {'friendId': ObjectId(friendId), 'directId' : ObjectId(directId), "friendName": friendName}}})
        mycol.update_one({"_id": ObjectId(friendId)}, {"$push": {"friends": { 'friendId': ObjectId(userId), 'directId' : ObjectId(directId), "friendName": username }}})
    except Exception as e:
        print(e)


def deleteQuery(coluna, procura, escolha):
    #Query
    global mydb
    mycol = getCol(mydb, escolha)
    myquery = { coluna: procura }
    mycol.delete_one(myquery)

