import jwt,hashlib
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

import datetime

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhanghae1
SECRET_KEY = '14조'


@app.route('/home')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.userInfo.find_one({"email": payload['id']})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))

@app.route('/')
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
                   'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': token, 'msg': 'success'})

    return jsonify({'msg':'Not available'})


#댓글 저장하기
@app.route('/api/comment_save', methods=['POST'])
def comment_save():
    if request.method == 'POST':
        comment_receive = request.form['comment']
        thumbnail_receive = request.form['thumbnail']
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.userInfo.find_one({"email": payload['id']})
            user_name = user_info['name']
            doc = {
                'content': comment_receive,
                'user_name': user_name,
                'thumbnail': thumbnail_receive
            }
            db.comments.insert_one(doc)
            return jsonify({'msg': '댓글이 등록되었습니다.'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


#댓글 10개씩 보이도록
@app.route('/api/comment_read', methods=['GET'])
def comment_read():
    if request.method == 'GET':
        comments = list(db.comments.find({}))
        res = list(map(lambda item: {'_id': str(item["_id"]),'content':item['content'],'user_name':item['user_name'],'thumbnail':item['thumbnail'],'like_num':db.commentLike.count_documents({'comment_id':str(item["_id"])})}, comments))
        return jsonify({'all_comments': res})


#댓글 좋아요
@app.route('/api/comment_like', methods=['POST'])
def comment_like():
    if request.method == 'POST':
        comment_id = request.form['comment_id']
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.userInfo.find_one({"email": payload['id']})
            user_id = user_info['email']
            like_checker = db.commentLike.find_one({'comment_id':comment_id,'user_id':user_id})
            if not like_checker:
                doc = {
                    'comment_id':comment_id,
                    'user_id': user_id
                }
                db.commentLike.insert_one(doc)
                like_num = db.commentLike.count_documents({'comment_id':comment_id})
                return jsonify({'like_num': like_num})
            else:
                db.commentLike.delete_one({'comment_id':comment_id,'user_id':user_id})
                like_num = db.commentLike.count_documents({'comment_id':comment_id})
                return jsonify({'like_num': like_num})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)