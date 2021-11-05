import math
import random

import jwt,hashlib
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

import datetime

import crawring_def

import collections

from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.login_prac

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


@app.route('/api/signout', methods=['POST'])
def signout():
    token_given = request.form['token']

    decoded_token = jwt.decode(token_given, SECRET_KEY, algorithms="HS256")
    user_id = decoded_token['id']

    db.userInfo.remove({'email': user_id})

    return jsonify({'msg': '탈퇴 완료!'})


@app.route('/api/account/check_up', methods=['POST'])
def valid_checker():
    email = request.form['email_give']
    checking_email = db.userInfo.find_one({'email': email}, {'_id': False})

    if checking_email is not None:
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

    return jsonify({'msg': 'Not available'})

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
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.userInfo.find_one({"email": payload['id']})
            user_id = user_info['email']
            res = list(map(lambda item: {'_id': str(item["_id"]),'content':item['content'],'user_name':item['user_name'],'thumbnail':item['thumbnail'],'like_num':db.commentLike.count_documents({'comment_id':str(item["_id"])}), 'color':'likeBtn_color' if db.commentLike.find_one({'comment_id':str(item["_id"]),'user_id':user_id}) else 'unlikeBtn_color'}, comments))
            return jsonify({'all_comments': res})   
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        


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
                return jsonify({'like_num': like_num, 'color': 'blue'})
            else:
                db.commentLike.delete_one({'comment_id':comment_id,'user_id':user_id})
                like_num = db.commentLike.count_documents({'comment_id':comment_id})
                return jsonify({'like_num': like_num, 'color':'grey'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/api/video/save', methods=['POST'])
def video_save():

    videoUrl = request.form['videoUrl']
    checking_videoUrl = db.videos.find_one({'videoUrl': videoUrl}, {'_id': False})

    if (checking_videoUrl is not None):
        return jsonify({'msg': 'Not available'})

    videoTitle = crawring_def.crawring_subject(videoUrl)
    embedUrl = crawring_def.crawring_embedUrl(videoUrl)
    videoThumbnail = crawring_def.crawring_thumbnailUrl(videoUrl)
    youtuber = crawring_def.crawring_youtuber(videoUrl)
    doc = {
        'videoUrl' : videoUrl,
        'videoTitle' : videoTitle,
        'embedUrl' : embedUrl,
        'videoThumbnail' : videoThumbnail,
        'youtuber':youtuber
    }

    db.videos.insert_one(doc)

    return jsonify({'msg': 'success'})


@app.route('/api/video/load', methods=['GET'])
def video_load():
    videos = list(db.videos.find({}, {'_id': False}))

    randomNumber = math.floor(random.random() * len(videos))

    videoTitle = videos[randomNumber]['videoTitle']
    embedUrl = videos[randomNumber]['embedUrl']
    videoThumbnail = videos[randomNumber]['videoThumbnail']
    videoUrl = videos[randomNumber]['videoUrl']
    youtuber = videos[randomNumber]['youtuber']

    return jsonify({'videoTitle': videoTitle, 'embedUrl': embedUrl, 'videoThumbnail': videoThumbnail, 'videoUrl':videoUrl, 'youtuber':youtuber})


#댓글 랭킹 api
@app.route('/api/comment_ranking', methods=['GET'])
def comment_ranking():
    if request.method == 'GET':
        comments = db.commentLike.find({},{'_id':False,'user_id':False})
        count = []
        for comment in comments:
            count.append(comment['comment_id'])
        rankings = collections.Counter(count).most_common(3)
        comment_rank1_id = rankings[0][0]
        comment_rank2_id = rankings[1][0]
        comment_rank3_id = rankings[2][0]
        comment_rank1 = db.comments.find_one({'_id':ObjectId(comment_rank1_id)})
        comment_rank2 = db.comments.find_one({'_id':ObjectId(comment_rank2_id)})
        comment_rank3 = db.comments.find_one({'_id':ObjectId(comment_rank3_id)})
        rankers = []
        rankers.append(comment_rank1)
        rankers.append(comment_rank2)
        rankers.append(comment_rank3)
        res = list(map(lambda item: {'_id': str(item["_id"]), 'content': item['content'], 'user_name': item['user_name'], 'thumbnail': item['thumbnail'], 'like_num': db.commentLike.count_documents({'comment_id': str(item["_id"])})}, rankers))
        return jsonify({'rankers': res})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
