from flask import Flask
from flask_pymongo import PyMongo
from pymongo import errors

app = Flask(__name__)
app.secret_key = "passwordGoesHere"
app.config["MONGO_URI"] = "mongodb://localhost:27017/todolist"

try:
    mongo = PyMongo(app)
except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print(err)
