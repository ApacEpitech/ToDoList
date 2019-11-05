from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug import generate_password_hash, check_password_hash


@app.route('/users', methods=['POST'])
def add_user():
    _json = request.json
    _email = _json['mail']
    _password = _json['password']
    # validate the received values
    if _email and _password:
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        user_id = mongo.db.user.insert({'email': _email,
                                        'pwd': _hashed_password,
                                        'banned': False,
                                        'administrator': False})
        inserted_user = find_user(user_id)
        resp = jsonify(inserted_user)
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def users():
    all_users = mongo.db.user.find()
    resp = dumps(all_users)
    return resp


@app.route('/user/<id>', methods=['GET'])
def user(id):
    user_found = find_user(id)
    resp = dumps(user_found)
    return resp


@app.route('/user/connect', methods=['GET'])
def user_connect():
    _json = request.json
    _mail = _json['mail']
    _password = _json['password']
    _hashed_password = generate_password_hash(_password)
    user_found = mongo.db.user.find_one({'mail': _mail, 'password': _hashed_password})
    if user_found:
        resp = dumps(user_found)
        return resp
    else:
        return unauthorized()


@app.route('/update', methods=['PUT'])
def update_user():
    _json = request.json
    _id = _json['_id']
    _email = _json['email']
    _password = _json['pwd']
    _banned = _json['banned']
    _administrator = _json['administrator']
    # validate the received values
    if _email and _password and _id:
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save edits
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'email': _email,
                                           'pwd': _hashed_password,
                                           'banned': _banned,
                                           'administrator': _administrator
                                           }
                                  })
        updated_user = find_user(_id)
        resp = jsonify(updated_user)
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
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


@app.errorhandler(403)
def unauthorized():
    message = {
        'status': 403,
        'message': 'Unauthorized: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp


def find_user(user_id):
    user_found = mongo.db.user.find_one({'_id': ObjectId(user_id)})
    return user_found
