from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from functools import wraps
import bcrypt
import os
from bson import json_util, ObjectId
import json
import datetime
from calendar import monthrange
import sys


# Load dotenv file
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Start the flask App
app = Flask(__name__)
if str(sys.argv[0] == 'local'):
    app.secret_key = os.getenv("APP_SECRET")
else:
    app.secret_key = os.environ['APP_SECRET']
CORS(app, supports_credentials=True)

# Setup the DB
if str(sys.argv[0]) == 'local':
    app.config['MONGODBNAME'] = os.getenv("DB_HOST")
    app.config['MONGO_URI'] = os.getenv("DB_URL")
else:
    app.config['MONGODBNAME'] = os.environ['DB_HOST']
    app.config['MONGO_URI'] = os.environ['DB_URL']
mongo = PyMongo(app)


# Routes protection decorator
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return jsonify({"message": "Please login first"})
        return fn(*args, **kwargs)
    return wrapper


# Routes
@app.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login_post():
    if 'username' in session.keys():
        return jsonify({"message": 'logged in'})
    body = request.get_json()
    users = mongo.db.budgeteer
    user = users.find_one({'username': body['username'].lower()})
    if user:
        if bcrypt.hashpw(body['password'].encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
            session.permanent = True
            session['username'] = body['username'].lower()
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
    user = users.find_one({'username': body['username'].lower()})
    years = [str(datetime.date.today().year), str(
        datetime.date.today().year + 1), str(datetime.date.today().year + 2)]
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    db_body = {}
    for year in years:
        db_body[year] = {}
        for i, month in enumerate(months):
            db_body[year][month] = {}
            for day in range(1, list(monthrange(int(year), int(i + 1)))[1]):
                db_body[year][month].update({str(day): {}})
    if user is None:
        users.insert_one(
            {
                'username': body['username'].lower(),
                'password': password_hashed,
                'config': {
                    'income': [],
                    'outcome': []
                },
                'budget': db_body
            })
    return jsonify({"message": 'account created'})


@app.route('/config/<type>', methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def get_config(type):
    if type != "income" and type != "outcome":
        return jsonify({"message": "invalid request"})
    users = mongo.db.budgeteer
    user = users.find_one({"username": session['username']})
    return jsonify({"message": list(user['config'][str(type)])})


@app.route('/config/<type>', methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def post_config(type):
    if type != "income" and type != "outcome":
        return jsonify({"message": "invalid request"})
    body = request.get_json()
    users = mongo.db.budgeteer
    if type == 'income':
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'config.income': body['transaction']
            }
        })
    if type == 'outcome':
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'config.outcome': body['transaction']
            }
        })
    db_body = create_transactions(type, body['transaction'])
    return jsonify({"message": db_body})


def create_transactions(type, transactions):
    years = [str(datetime.date.today().year), str(
        datetime.date.today().year + 1), str(datetime.date.today().year + 2)]
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    if type == 'income':
        sign = 1
    if type == 'outcome':
        sign = -1
    body = {}
    for tx in transactions:
        print(tx)
        if tx[1] == 'Mensuel':
            for year in years:
                if year not in body:
                    body[year] = {}
                for i in range(tx[5][1] - 1, len(months)):
                    if months[i] not in body[year]:
                        body[year][months[i]] = {}
                    if tx[2] not in body[year][months[i]]:
                        body[year][months[i]][tx[2]] = {}
                    body[year][months[i]][tx[2]].update(
                        {tx[3]: int(tx[4]) * sign})
                tx[5][1] = 1

        if tx[1] == 'Bi-hebdo':
            days_to_add = 14
        if tx[1] == 'Hebdo':
            days_to_add = 7
        if tx[1] == 'Bi-hebdo' or tx[1] == 'Hebdo':
            current_year = tx[5][0]
            counter = 1
            for year in years:
                if year not in body:
                    body[year] = {}
                if counter == 1:
                    month = tx[5][1]
                else:
                    month = 1
                if counter == 1:
                    day = tx[5][2]
                    counter = 2

                while current_year == year:
                    if months[month - 1] not in body[year]:
                        body[year][months[month - 1]] = {}
                    if day not in body[year][months[month - 1]]:
                        body[year][months[month - 1]][day] = {}
                    body[year][months[month - 1]
                               ][day].update({tx[3]: tx[4] * sign})
                    new_date = datetime.datetime.strptime(
                        str(year) + " " + str(month) + " " + str(day), '%Y %m %d')
                    new_date = new_date + datetime.timedelta(days=days_to_add)
                    current_year = str(new_date.year)
                    month = new_date.month
                    day = str(new_date.day)
                    print(year, day)
    print(json.dumps(body))
    return body


# Automatically run the auto reload server by only running the script
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True, port=3000)
