from flask import Flask
from flask_pymongo import PyMongo
from pymongo import errors
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = ""
app.config["MONGO_URI"] = "mongodb://localhost:27017/todolist"
CORS(app, resources={r"/*": {"origins": "*"}})


try:
    mongo = PyMongo(app)
except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print(err)
