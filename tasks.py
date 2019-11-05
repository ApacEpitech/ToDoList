from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request


@app.route('/tasks', methods=['POST'])
def add_task():
    _json = request.json
    _title = _json['mail']
    _user = _json['user_id']
    # validate the received values
    if _title:
        # save details
        task_id = mongo.db.task.insert({'title': _title,
                                        'content': '',
                                        'user_id': _user,
                                        'done': False})
        inserted_task = find_task(task_id)
        resp = jsonify(inserted_task)
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/tasks', methods=['GET'])
def tasks():
    all_tasks = mongo.db.task.find()
    resp = dumps(all_tasks)
    return resp


@app.route('/task/<id>', methods=['GET'])
def task(id):
    task_found = find_task(id)
    resp = dumps(task_found)
    return resp


@app.route('/tasks/<user_id>', methods=['GET'])
def tasks(user_id):
    tasks_found = mongo.db.task.find({'user_id': ObjectId(user_id)})
    resp = dumps(tasks_found)
    return resp


@app.route('/update', methods=['PUT'])
def update_task():
    _json = request.json
    _id = _json['_id']
    _title = _json['email']
    _content = _json['pwd']
    _user = _json['user_id']
    _done = _json['done']
    # validate the received values
    if _title and _id:
        # save edits
        mongo.db.task.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'title': _title,
                                           'content': _content,
                                           'done': _done,
                                           'user_id': _user
                                           }
                                  })
        updated_task = find_task(_id)
        resp = jsonify(updated_task)
        resp.status_code = 200
        return resp
    else:
        return bad_request()


@app.route('/delete/<id>', methods=['DELETE'])
def delete_task(id):
    mongo.db.task.delete_one({'_id': ObjectId(id)})
    resp = ''
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found():
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.errorhandler(401)
def bad_request():
    message = {
        'status': 401,
        'message': 'Bad request: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 401

    return resp


def find_task(task_id):
    task_found = mongo.db.task.find_one({'_id': ObjectId(task_id)})
    return task_found
