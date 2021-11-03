import jwt,hashlib
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

import datetime

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.login_prac


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/api/account', methods=['POST'])
def api_register():
    email = request.form['email_give']
    pw = request.form['pw_give']
    name = request.form['name_give']

    pw_encrypt = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    doc = {
        'email': email,
        'password': pw_encrypt,
        'name': name
    }

    db.userInfo.insert_one(doc)

    return jsonify({'msg': 'success'})


@app.route('/api/account/check_up', methods=['POST'])
def valid_checker():
    email = request.form['email_give']
    checking_email = db.userInfo.find_one({'email': email}, {'_id': False})

    if(checking_email is not None):
        return jsonify({'msg': 'Not available'})

    return jsonify({'msg': 'available'})


@app.route('/api/login', methods=['POST'])
def token_maker():
    email = request.form['email']
    pw = request.form['password']

    pw_encrypt = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    findingResult = db.userInfo.find_one({'email': email, 'password': pw_encrypt}, {'_id': False})

    if(findingResult is not None):
        payload = {'id': email,
                   'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)}
        token = jwt.encode(payload, '14조', algorithm='HS256').decode('utf-8')

        return jsonify({'token': token, 'msg': 'success'})

    return jsonify({'msg':'Not available'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)