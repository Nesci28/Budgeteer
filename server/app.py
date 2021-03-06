from flask import Flask, render_template, url_for, request, session, redirect, jsonify, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from functools import wraps
import bcrypt
import os
from bson import json_util, ObjectId
import json
import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time


# Load dotenv file
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Start the flask App
app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
app.secret_key = os.environ['APP_SECRET']
CORS(app, supports_credentials=True)

# Setup the DB
app.config['MONGODBNAME'] = os.environ['DB_HOST']
app.config['MONGO_URI'] = os.environ['DB_URL']
mongo = PyMongo(app)

# Setup the cronjob


def send_emails():
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    users = mongo.db.budgeteer
    users = users.find({}, {"_id": 0, "history": 1, "emails": 1})
    year = str(datetime.date.today().year)
    month = months[datetime.date.today().month - 1]
    day = str(datetime.date.today().day)
    for user in users:
        history = user["history"][year][month][day]
        if len(history) > 0:
            content = ""
            for tx in history:
                content += tx["title"] + " - " + str(tx["value"]) + "\n"
            message = {
                'personalizations': [
                    {
                        'to': [],
                        'subject': 'Budgeteer | Daily Report'
                    }
                ],
                'from': {
                    'email': 'budgeteer@nos.com'
                },
                'content': [
                    {
                        'type': 'text/plain',
                        'value': content
                    }
                ]
            }
            for add in user["emails"]:
                message["personalizations"][0]["to"].append({'email': add})
            try:
                SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            except Exception as e:
                print(e)


scheduler = BackgroundScheduler()
job = scheduler.add_job(send_emails, 'interval', seconds=1 * 60 * 60 * 24)
scheduler.start()

# Routes protection decorator


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return jsonify({"message": "Please login first"})
        return fn(*args, **kwargs)
    return wrapper


# Routes
@app.route('/api/v2/login', methods=["POST"])
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
            check_recalculation()
            return jsonify({"message": 'logged in'})
    return jsonify({"message": 'invalid credentials'})


@app.route('/api/v2/login', methods=["GET"])
@cross_origin(supports_credentials=True)
def login_get():
    if 'username' in session.keys():
        check_recalculation()
        return jsonify({"message": 'logged in'})
    return jsonify({"message": 'not logged in'})


@app.route('/api/v2/logout', methods=["GET"])
@cross_origin(supports_credentials=True)
def sign_out():
    session.pop('username')
    return jsonify({"message": 'logged out'})


@app.route('/api/v2/register', methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    body = request.get_json()
    password = body['password']
    password = bytes(password, encoding="ascii")
    password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    password_hashed = password_hashed.decode('ascii')
    users = mongo.db.budgeteer
    user = users.find_one({'username': body['username'].lower()})
    if user is not None:
        return jsonify({"message": 'Username already taken'})
    years = [str(datetime.date.today().year), str(
        datetime.date.today().year + 1), str(datetime.date.today().year + 2)]
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    db_body = {}
    db_budget = {}
    for year in years:
        db_body[year] = {}
        for i, month in enumerate(months):
            db_body[year][month] = {}
            for day in range(1, list(monthrange(int(year), int(i + 1)))[1] + 1):
                db_body[year][month].update({str(day): []})
    for year in years:
        db_budget[year] = {}
        for i, month in enumerate(months):
            db_budget[year][month] = []

    if user is None:
        users.insert_one(
            {
                'username': body['username'].lower(),
                'password': password_hashed,
                'config': {
                    'income': [],
                    'outcome': [],
                    'budget': []
                },
                'budget': db_budget,
                'history': db_body
            })
    return jsonify({"message": 'account created'})


@app.route('/api/v2/account/<year>', methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def get_account(year):
    users = mongo.db.budgeteer
    user = users.find_one({"username": session['username']})
    return jsonify({"message": user['history'][str(year)]})


@app.route('/api/v2/config/<type>', methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def get_config(type):
    if type != "income" and type != "outcome" and type != "budget":
        return jsonify({"message": "invalid request"})
    users = mongo.db.budgeteer
    user = users.find_one({"username": session['username']})
    return jsonify({"message": list(user['config'][str(type)])})


@app.route('/api/v2/config/<type>', methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def post_config(type):
    if type != "income" and type != "outcome" and type != "budget":
        return jsonify({"message": "invalid request"})
    body = request.get_json()
    users = mongo.db.budgeteer
    if body['type'] == 'add':
        add_transaction(type, users, body)
        return jsonify({"message": 'transaction added'})
    if body['type'] == 'remove':
        remove_transaction(type, users, body)
        return jsonify({"message": 'transaction removed'})
    if body['type'] == 'budget_save':
        budget = users.find_one({"username": session['username']})
        budget = budget["config"]["budget"]
        budget[body['index']]["value"] = body['value']
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'config.budget': budget
            }
        })
    if body['type'] == 'budget_remove':
        budget = users.find_one({"username": session['username']})
        budget = budget['config']['budget']
        budget.pop(body['index'])
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'config.budget': budget
            }
        })
        return jsonify({"message": 'budget removed'})
    if body['type'] == 'budget_add':
        budget = users.find_one({"username": session['username']})
        budget = budget['config']['budget']
        for el in budget:
            if body['title'].lower() in el.values():
                return jsonify({"message": "category already exist"})
        budget.append({"title": body['title'].lower(), "value": body['value']})
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'config.budget': budget
            }
        })
        return jsonify({"message": 'budget added'})


@app.route('/api/v2/budget', methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def get_budget():
    body = request.get_json()
    month = int(body['month'])
    year = body['year']
    month_budget = calcul_monthly(month, year)
    return jsonify({"message": {
        'last_month': month_budget['last_month'],
        'tx_month': month_budget['tx_month'],
        'month_budget': month_budget['month_budget']
    }})


@app.route('/api/v2/getType', methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def get_type():
    users = mongo.db.budgeteer
    user = users.find_one({"username": session['username']})
    titles = []
    for title in user['config']['budget']:
        titles.append(title['title'])
    return jsonify({"message": titles})


@app.route('/api/v2/addTx', methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def add_tx():
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    body = request.get_json()
    users = mongo.db.budgeteer
    query = {}
    query['history.' + str(body['year']) + "." + months[body['month']] +
          "." + str(body['day'])] = {"title": body['title'], "value": float(body['value']), "type": "budget"}
    users.find_one_and_update({
        "username": session['username']
    }, {
        '$push': query
    })
    return jsonify({"message": 'tx added'})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


def calcul_monthly(month, year):
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    users = mongo.db.budgeteer
    user = users.find_one({"username": session['username']})
    last_month = None
    if month == 0:
        year = str(int(year) - 1)
        last_month = 11
    if last_month == None:
        last_month = month - 1
    last_month = months[last_month]

    # Getting the budget configurations
    budget_configs = user['config']['budget']
    last_month_tx = user['budget'][str(year)][last_month]
    current_month_tx = user['history'][str(year)][months[month]]

    # Calculate the results of last month only if the last month is  completely passed
    today = datetime.datetime.today()
    current_month = today.month
    if last_month_tx == [] and month + 1 == current_month:
        last_month_tx = calculate_last_month(year, month - 1)

    # Updating the budget values with the last month values
    # last_month_tx == resuls of the last month budgets
    # budget_configs == budget base configurations
    for budget in budget_configs:
        for tx in last_month_tx:
            if budget['title'] == tx['title']:
                budget['value'] = float(budget['value']) + float(tx['value'])

    month_budget = budget_configs

    # Updating the budget by going through each day of the month
    # current_month_tx == current month transactions dict with list for each day
    # month_budget == the result of the configs budget - the leftovers from last month in a list
    for budget in month_budget:
        for tx in current_month_tx:
            tx = current_month_tx[tx]
            if len(tx) > 0:
                for each_tx in tx:
                    if budget['title'] == each_tx.get('title'):
                        budget['value'] = budget['value'] - \
                            each_tx['value']

    return {
        'last_month': last_month_tx,
        'tx_month': current_month_tx,
        'month_budget': month_budget
    }


def calculate_last_month(year, last_month):
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    users = mongo.db.budgeteer
    db = users.find_one({"username": session['username']})
    configs = db['config']['budget']
    last_month_tx = db['history'][str(year)][months[last_month]]
    res = []
    for config in configs:
        default_value = config['value']
        res.append({"title": config['title'], "value": config['value']})
        for tx in last_month_tx:
            tx = last_month_tx[tx]
            if tx != []:
                if config['title'] == tx['title']:
                    res[-1]['value'] = res[-1]['value'] - tx['value']
        if res[-1]['value'] == default_value:
            res[-1]['value'] = 0

    query = {}
    query['budget.' + str(year) + '.' + months[last_month]] = res
    users.find_one_and_update({"username": session['username']}, {
        '$set': query
    })
    return res


def check_recalculation():
    users = mongo.db.budgeteer
    current_db = users.find_one({"username": session['username']})
    db_years = list(current_db['history'].keys())
    year = datetime.datetime.today().year + 3
    if int(db_years[-1]) < year:
        months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
                  'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
        db_body = {}
        db_body[str(year)] = {}
        for i, month in enumerate(months):
            db_body[str(year)][month] = {}
            for day in range(1, list(monthrange(int(year), int(i + 1)))[1] + 1):
                db_body[str(year)][month].update({str(day): []})
        income_tx = current_db['config']['income']
        for tx in income_tx:
            updated_db_body = create_transactions('income', tx)
            for el in updated_db_body:
                if el[0] == str(year):
                    db_body[el[0]][el[1]][el[2]].append({el[3]: el[4] * 1})

        outcome_tx = current_db['config']['outcome']
        for tx in outcome_tx:
            updated_db_body = create_transactions('income', tx)
            for el in updated_db_body:
                if el[0] == str(year):
                    db_body[el[0]][el[1]][el[2]].append({el[3]: el[4] * -1})

        current_db_body = current_db['history']
        current_db_body[str(year)] = db_body[str(year)]
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'history': current_db_body
            }
        })
    return


def add_transaction(type, users, body):
    if type == 'income':
        users.find_one_and_update({"username": session['username']}, {
            '$addToSet': {
                'config.income': body['transaction']
            }
        })
    if type == 'outcome':
        users.find_one_and_update({"username": session['username']}, {
            '$addToSet': {
                'config.outcome': body['transaction']
            }
        })
    updated_db_body = create_transactions(type, body['transaction'])
    current_db_body = users.find_one({"username": session['username']})
    current_db_body = current_db_body['history']
    for tx in updated_db_body:
        current_db_body[tx[0]][tx[1]][str(int(tx[2]))].append(
            {"title": tx[3], "value": tx[4]})
    users.find_one_and_update({"username": session['username']}, {
        '$set': {
            'history': current_db_body
        }
    })


def remove_transaction(type, users, body):
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    list_of_tx = create_transactions(type, body['transaction'])
    current_db_body = users.find_one({"username": session['username']})
    current_db_body = current_db_body['history']
    for tx in list_of_tx:
        new_date = datetime.datetime.strptime(
            str(tx[0]) + " " + str(months.index(tx[1]) + 1) + " " + str(tx[2]), '%Y %m %d')
        if datetime.datetime.today() <= new_date:
            current_db_body[tx[0]][tx[1]][str(
                int(tx[2]))].remove({"title": tx[3], "value": tx[4]})

    users.find_one_and_update({"username": session['username']}, {
        '$set': {
            'history': current_db_body
        }
    })
    if type == 'income':
        id_to_remove = body['transaction'][0]
        current_db_config = users.find_one({"username": session['username']})
        current_db_config = current_db_config['config']['income']
        current_db_config.pop(id_to_remove)
        for tx in current_db_config:
            tx[0] = len(current_db_config) - 1
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'config.income': current_db_config
            }
        })

    if type == 'outcome':
        id_to_remove = body['transaction'][0]
        current_db_config = users.find_one({"username": session['username']})
        current_db_config = current_db_config['config']['income']
        current_db_config.pop(id_to_remove)
        for tx in current_db_config:
            tx[0] = len(current_db_config) - 1
        users.find_one_and_update({"username": session['username']}, {
            '$set': {
                'config.outcome': current_db_config
            }
        })


def create_transactions(type, tx):
    years = [str(datetime.date.today().year), str(
        datetime.date.today().year + 1), str(datetime.date.today().year + 2)]
    months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
    if type == 'income':
        sign = 1
    if type == 'outcome':
        sign = -1
    body = []
    if tx[1] == 'Trimestriel':
        new_date = datetime.datetime.strptime(
            tx[5][0] + " " + str(tx[5][1]) + " " + str(tx[5][2]), '%Y %m %d')
        while new_date.year <= int(years[-1]):
            body.append(
                [str(new_date.year), str(new_date.month), tx[2], tx[3], float(tx[4]) * sign])
            new_date = new_date + relativedelta(months=3)
            print(new_date.year, int(years[-1]))

    if tx[1] == 'Mensuel':
        new_date = datetime.datetime.strptime(
            tx[5][0] + " " + str(tx[5][1]) + " " + str(tx[5][2]), '%Y %m %d')
        while new_date.year <= int(years[-1]):
            body.append(
                [str(new_date.year), str(new_date.month), tx[2], tx[3], float(tx[4]) * sign])
            new_date = new_date + relativedelta(months=1)

    if tx[1] == 'Bimensuel':
        new_date = datetime.datetime.strptime(
            tx[5][0] + " " + str(tx[5][1]) + " " + str(tx[5][2]), '%Y %m %d')
        while new_date.year <= int(years[-1]):
            body.append(
                [str(new_date.year), str(new_date.month), str(new_date.day), tx[3], float(tx[4]) * sign])
            last_day_of_month = monthrange(
                new_date.year, new_date.month)[1]
            body.append(
                [str(new_date.year), str(new_date.month), str(last_day_of_month), tx[3], float(tx[4]) * sign])
            new_date = new_date + relativedelta(months=1)

    if tx[1] == 'Quinzomadaire':
        days_to_add = 14
    if tx[1] == 'Hebdo':
        days_to_add = 7
    if tx[1] == 'Quotidien':
        days_to_add = 1
    if tx[1] == 'Quinzomadaire' or tx[1] == 'Hebdo' or tx[1] == 'Quotidien':
        new_date = datetime.datetime.strptime(
            tx[5][0] + " " + str(tx[5][1]) + " " + str(tx[5][2]), '%Y %m %d')
        while new_date.year <= int(years[-1]):
            body.append(
                [str(new_date.year), str(new_date.month), str(new_date.day), tx[3], float(tx[4]) * sign])
            new_date = new_date + datetime.timedelta(days=days_to_add)

    return body


# Automatically run the auto reload server by only running the script
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    cls()
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True, port=3000)
