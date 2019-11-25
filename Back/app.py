from flask import Flask
from flask_pymongo import PyMongo
from pymongo import errors
from flask_cors import CORS
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = ""
app.config["MONGO_URI"] = "mongodb://localhost:27017/todolist"
CORS(app, resources={r"/*": {"origins": "*"}})

try:
    mongo = PyMongo(app)
    user_found = mongo.db.user.find_one({'email': "admin@admin.com"})
    if user_found is None:
        mongo.db.user.insert({'email': "admin@admin.com",
                                            'pwd': generate_password_hash("admin"),
                                            'banned': False,
                                            'administrator': True})
except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print(err)
