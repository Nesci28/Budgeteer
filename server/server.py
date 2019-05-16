from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import bcrypt
import os
from bson import json_util, ObjectId
import json
import time


# Load dotenv file
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Start the flask App
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")
CORS(app, support_credentials=True)

# Setup the DB
app.config['MONGODBNAME'] = os.getenv("DB_HOST")
app.config['MONGO_URI'] = os.getenv("DB_URL")
mongo = PyMongo(app)

# Routes
@app.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login_post():
    if 'username' in session.keys():
        return jsonify({"message": 'logged in'})
    body = request.get_json()
    users = mongo.db.budgeteer
    user = users.find_one({'username': body['username']})
    if user:
        if bcrypt.hashpw(body['password'].encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
            session.permanent = True
            session['username'] = body['username']
            return jsonify({"message": 'logged in'})
    return jsonify({"message": 'invalid credentials'})


@app.route('/login', methods=["GET"])
@cross_origin(supports_credentials=True)
def login_get():
    if 'username' in session.keys():
        return jsonify({"message": 'logged in'})
    return jsonify({"message": 'not logged in'})


@app.route('/logout', methods=["GET"])
@cross_origin(supports_credentials=True)
def sign_out():
    print(session)
    session.pop('username')
    return jsonify({"message": 'logged out'})


@app.route('/register', methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    body = request.get_json()
    password = body['password']
    password = bytes(password, encoding="ascii")
    password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    password_hashed = password_hashed.decode('ascii')
    users = mongo.db.budgeteer
    user = users.find_one({'username': body['username']})
    if user is None:
        users.insert_one(
            {'username': body['username'], 'password': password_hashed})
    return jsonify({"message": 'account created'})


# Automatically run the auto reload server by only running the script
if __name__ == '__main__':
    app.run(debug=True)
