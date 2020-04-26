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

@app.route('/tasks', methods = ['GET'])
def get_task():

    output = []

    for key in db.meals.find():
        output.append(key)

    return Response(dumps(output), status=200, mimetype='application/json')


@app.route('/tasks/open', methods = ['GET'])
def open_tasks():
    output = []

    for key in db.meals.find({'is_completed':False}):
        output.append(key)

    return Response(dumps(output), status=200, mimetype='application/json')


@app.route('/tasks/closed', methods = ['GET'])
def closed_tasks():
    output = []

    for key in db.meals.find({'is_completed':True}):
        output.append(key)

    return Response(dumps(output), status=200, mimetype='application/json')

@app.route('/tasks/open/<name>', methods = ['POST'])
def update_open_tasks(name):

    db.meals.update({'_id': ObjectId(name) }, {"$set": {"is_completed":False}})

    return Response(dumps(name), status = 204)

@app.route('/tasks/closed/<name>', methods = ['POST'])
def update_closed_tasks(name):

    db.meals.update({'_id': ObjectId(name) }, {"$set": {"is_completed":True}})

    return Response("", status = 204)

@app.route('/tasks/delete/<name>', methods=['DELETE'])
def delete_tasks(name):
    db.meals.remove({'_id': ObjectId(name)})
    return Response("", status = 204)








    









