import re
from bson import Binary, Code
from bson.json_util import dumps
from bson import ObjectId
from flask import Flask, request, Response
import json
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/tasks"

mongo = PyMongo(app)
db = mongo.db


# Get all tasks
@app.route('/tasks', methods = ['GET'])
def get_task():

    output = []

    for key in db.meals.find():
        output.append(key)

    return Response(dumps(output), status=200, mimetype='application/json')

# Get all open tasks
@app.route('/tasks/open', methods = ['GET'])
def open_tasks():
    output = []

    for key in db.meals.find({'is_completed':False}):
        output.append(key)

    return Response(dumps(output), status=200, mimetype='application/json')

# Get all closed tasks
@app.route('/tasks/closed', methods = ['GET'])
def closed_tasks():
    output = []

    for key in db.meals.find({'is_completed':True}):
        output.append(key)

    return Response(dumps(output), status=200, mimetype='application/json')

# Update task as not completed
@app.route('/tasks/open/<name>', methods = ['POST'])
def update_open_tasks(name):

    # Checking if objectid is valid
    if not bool(re.match("^[0-9a-fA-F]{24}$",name)):
        return Response(json.dumps({'error': 'Invalid Objectid'}), status=404)

    # Task Update
    a = db.meals.update({'_id': ObjectId(name) }, {"$set": {"is_completed":False}})


    # Updation Status and response
    if a['nModified'] == 1:
        return Response("", status = 204)
    else:
        if a['n'] == 1:
            return Response("The tasks is already open", status=200)
        else:
            return Response(json.dumps({'error': 'Object not found'}), status=404)
    return Response(dumps(name), status = 204)

# Update task as completed
@app.route('/tasks/closed/<name>', methods = ['POST'])
def update_closed_tasks(name):

    if not bool(re.match("^[0-9a-fA-F]{24}$",name)):
        return Response(json.dumps({'error': 'Invalid Objectid'}), status=404)

    a = db.meals.update({'_id': ObjectId(name) }, {"$set": {"is_completed":True}})

    if a['nModified'] == 1:
        return Response("", status = 204)
    else:
        if a['n'] == 1:
            return Response("The tasks is already closed", status=200)
        else:
            return Response(json.dumps({'error': 'Object not found'}), status=404)

# Delete task
@app.route('/tasks/delete/<name>', methods=['DELETE'])
def delete_tasks(name):

    if not bool(re.match("^[0-9a-fA-F]{24}$",name)):
        return Response(json.dumps({'error': 'Invalid Objectid'}), status=404)

    a = db.meals.remove({'_id': ObjectId(name)})

    if a['n'] == 1:
        return Response("", status = 204)
    else:
        return Response(json.dumps({'error': 'Object not found'}), status=404)








    









