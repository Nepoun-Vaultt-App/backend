from flask import Flask, request
from modules.database import insert, findSort, findMultipleQuery, findQuery, findAll, updateQuery, deleteQuery, pushNewMessage, addNewFriend
from bson.objectid import ObjectId
import jsonpickle
import json

app = Flask(__name__)

# convert recursively all ObjectIds to strings in a dictionary
def obj_to_str(data):
    if isinstance(data, dict):
        return {obj_to_str(key): obj_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [obj_to_str(element) for element in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def removeTableId(dict, whatToRemove):
	dict.pop(whatToRemove)
	return dict

@app.route('/create', methods=['POST'])
def create():
	content_type = request.headers.get('Content-type')

	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			id = json["TABLE_ID"]
			obj = removeTableId(json, "TABLE_ID")
			result = insert(id, obj)
			
			return 'success'
		except Exception as e: 
			return e


	
@app.route('/getAll', methods=['GET', 'POST'])
def getAll():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			print(json)
			id = json["TABLE_ID"]
			return jsonpickle.dumps(findAll(id))
		except Exception as e:
			print(dict(request.json))
			return e

@app.route('/getById', methods=['GET', 'POST'])
def getById():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			print(json)
			id = json["TABLE_ID"]
			data = findQuery(id, "_id", ObjectId(json["_id"]))
			#del data["_id"]
			
			return jsonpickle.dumps(data)
		except Exception as e:
			return e


@app.route("/getDirect", methods=['GET', 'POST'])
def getDirect():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			data = findQuery(3, "_id", ObjectId(request.json))
			return jsonpickle.dumps(data)
		except Exception as e:
			return e
		
@app.route('/getByColumn', methods=['GET', 'POST'])
def getByColumn():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			id = json["TABLE_ID"]
			data = findQuery(id, json['_column'], json["_value"])
			data["_id"] = str(data["_id"])
			return jsonpickle.dumps(data)
		except Exception as e:
			return e

@app.route('/getAllByColumn', methods=['GET', 'POST'])
def getAllByColumn():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			id = json["TABLE_ID"]
			data = findMultipleQuery(id, json['_column'], json["_value"])
			return jsonpickle.dumps(data)
		except Exception as e:
			return e


@app.route('/update', methods=['PUT'])
def update():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			print(json)
			table_id = json["TABLE_ID"]
			_id = str(json["_id"])
			del json["TABLE_ID"]
			del json["_id"]
			updateQuery(table_id, _id, json)
			
			return "success"
		except Exception as e: 
			return str(e)

@app.route('/delete', methods=['DELETE', 'POST'])
def deleteById():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			id = json["TABLE_ID"]
			deleteQuery("_id", ObjectId(json["_id"]), id)
			return "successful"
		except Exception as e:
			return e

@app.route("/login", methods=['POST'])
def login():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			tableId = 1
			lookForUser = findQuery(tableId, "username", json["username"])
			if(lookForUser):
				if json["password"] == lookForUser["password"]:

					return str(lookForUser["_id"])
				else:
					return "wrong password"
			else:
				return "user not found"

		except Exception as e:
			return e

@app.route("/pushMessage", methods=['PUT'])
def pushMessage():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			id = json["id"]
			json.pop("id")
			pushNewMessage(id, json)
			return "success"
		except Exception as e:
			return e

@app.route("/addFriend", methods=['PUT'])
def addFriend():
	content_type = request.headers.get('Content-type')
	if(content_type == "application/json"):
		try:
			json = dict(request.json)
			userId = str(json["userId"])
			query = findQuery(1, json["_column"], json["_value"])
			friendId = str(query["_id"])
			
			print(userId, " \n ", friendId)
			addNewFriend(userId, friendId, str(json["username"]), str(json["friendName"]))
			return "success"
		except Exception as e:
			return str(e)	

@app.route('/testConn', methods=['PUT', 'POST', 'GET', 'DELETE'])
def testConn():
	return "Connection is working fine"
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host="0.0.0.0", port=5000)