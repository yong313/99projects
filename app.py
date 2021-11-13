import math
import random

import jwt,hashlib

#hashlib 쓰는 것과 밑에 werkzeug.security쓰는 거는 비밀번호 설정할 때 무슨차이지?
#from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, g

app = Flask(__name__)
# session을 위한 암호화 키
app.secret_key = "14조"

import datetime

import crawring_def

import collections

from bson.objectid import ObjectId

from pymongo import MongoClient

from functools import wraps

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.login_prac

SECRET_KEY = '14조'

#서버기반인증방식

# 전역 객체 g를 app 라우트전에 추가하여 g를 사용할 수 있도록함 ==> g로 현재 로그인된 user의 정보 가져올 수 있음
# 전역 객체 g를 꼭 써야하나? 안쓰면 계속 session받는 함수 중복해서 써줘야됨 중복을 피하기 위해서는 g를 써주는게 좋을듯
# 근데 지금은 g안에 user밖에 없어서 굳이 한번 더 거치는 느낌이 있음 없어도 될듯?
@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.userInfo.find_one({"email": user_id})

# login어노테이션으로 한번에 쓰자
# def login_checker():
#     if g.user is None:
#         return redirect(url_for('login'))
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            # login하기 전 페이지로 가기 위한 변수 next
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



#로그인을 해야 열리는 메인페이지
@app.route('/home')
@login_required
def home():
    # print(request.cookies) 쿠키에 session이 담겨서 보내지는데 왜 브라우저엔 session이 안뜨지?
    # 쿠키의 name컬럼의 session에서 user_id를 받아옴 
    # 1. 그럼 request.cookies.get('session')해도 받을까? 그럼 암호화된 value를 받게 되는데 거기서 user_id를 디코딩해야되나?
    # 2. 1개뿐만아니라('user_Id'만 저장되있는 현재) 여러개를 session에 담아도 될까? 어떤 형태로 담기는 거지?
    # login_checker()
    user_info = g.user
    return render_template('index.html', user_info = user_info)


#로그인페이지 랜더링
@app.route('/')
def login():
    return render_template('login.html')

#회원가입페이지 랜더링
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

@app.route('/api/logout')
@login_required
def logout():
    # clear()가 요청을 보내는 사람의 브라우저에 있는 모든 session만 지우는 듯함 아마 user_id뿐만 아니라 다른것도 있었으면 pop()으로 골라서 지울 수도 있을듯
    # 또한 프론트에서 이 작업을 할 수 없는게 document.cookie를 하면 session이 잡히질 않음 (왜 쿠키에있지만 쿠키에 잡히질 않지?)
    session.clear()
    return jsonify({'ok': True})


@app.route('/api/signout')
@login_required
def signout():
    if g.user is None:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    db.userInfo.delete_one({'email': user_id})
    # session.clear()안 넣어도 되나? 안넣어도 되긴하는데 cookie의 session창에 남으니까 지워주자
    session.clear()
    return jsonify({'ok': True})


@app.route('/api/account/check_up', methods=['POST'])
def valid_checker():
    email = request.form['email_give']
    checking_email = db.userInfo.find_one({'email': email}, {'_id': False})

    if checking_email is not None:
        return jsonify({'msg': 'Not available'})

    return jsonify({'msg': 'available'})

#로그인시 토큰생성api
@app.route('/api/login', methods=['POST'])
def token_maker():
    #post방식으로 request시에만 등록
    if request.method == 'POST':
        #로그인 페이지에서 유저가 쓴 email, password받음
        email = request.form['email']
        pw = request.form['password']

        #유저 비밀번호 암호화
        pw_encrypt = hashlib.sha256(pw.encode('utf-8')).hexdigest()

        #로그인 페이지에서 유저가 쓴 email, password를 데이터베이스에서 확인
        user = db.userInfo.find_one({'email': email, 'password': pw_encrypt}, {'_id': False})
        #데이터베이스에 유저가 쓴 email과 password가 있을시 토큰생성
        if user:
            # 세션을 왜 clear()해주는 거지? 그 전에 있던 정보들을 없애면 로그인했던 사람들은 로그아웃되는거 아닌가?
            session.clear()
            session['user_id'] = user['email']
            # session이 쿠키에 자동으로 생성됨 토큰인증방식은 프론트에서 토큰을 받은 후 쿠키에 집어넣어 줬어야 했는데 session에 저장만하면 쿠키에 자동으로 생성
            return jsonify({'msg':'success'})
        #데이터베이스에 유저가 쓴 email과 password가 없을 시 세션에 아이디 저장실패
        return jsonify({'msg': 'Not available'})

#댓글 저장하기
@app.route('/api/comment_save', methods=['POST'])
@login_required
def comment_save():
    #post방식으로 request시에만 등록
    if request.method == 'POST':
        #form형식으로 comment내용, thumbnail주소를 받고 쿠키로 유저식별
        comment_receive = request.form['comment']
        thumbnail_receive = request.form['thumbnail']
        token_receive = request.cookies.get('mytoken')
        #로그인되었을 경우 댓글등록
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
        #로그인 안되었거나 토큰만료시 댓글등록 실패
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

#댓글 클라이언트사이드 랜더링
@app.route('/api/comment_read', methods=['GET'])
@login_required
def comment_read():
    #get형식으로 request올시에만 생성
    if request.method == 'GET':
        comments = list(db.comments.find({}))
        token_receive = request.cookies.get('mytoken')
        #로그인시 댓글관련 데이터 리턴
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.userInfo.find_one({"email": payload['id']})
            user_id = user_info['email']
            res = list(map(lambda item: {'_id': str(item["_id"]),'content':item['content'],'user_name':item['user_name'],'thumbnail':item['thumbnail'],'like_num':db.commentLike.count_documents({'comment_id':str(item["_id"])}), 'color':'likeBtn_color' if db.commentLike.find_one({'comment_id':str(item["_id"]),'user_id':user_id}) else 'unlikeBtn_color'}, comments))
            return jsonify({'all_comments': res})   
        #로그인 실패or토큰없을시 로그인페이지로
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        


#댓글 좋아요 클라이언트사이드랜더링
@app.route('/api/comment_like', methods=['POST'])
@login_required
def comment_like():
    if request.method == 'POST':
        comment_id = request.form['comment_id']
        token_receive = request.cookies.get('mytoken')
        #로그인시 댓글좋아요 수와 댓글을 색깔 리턴
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.userInfo.find_one({"email": payload['id']})
            user_id = user_info['email']
            like_checker = db.commentLike.find_one({'comment_id':comment_id,'user_id':user_id})
            #좋아요 안누른 상태일경우 눌렀을때 좋아요 데이터베이스에 추가해주고 색깔은 파란색으로
            if not like_checker:
                doc = {
                    'comment_id':comment_id,
                    'user_id': user_id
                }
                db.commentLike.insert_one(doc)
                like_num = db.commentLike.count_documents({'comment_id':comment_id})
                return jsonify({'like_num': like_num, 'color': 'blue'})
            #좋아요 누른상태일경우 눌렀을때 좋아요 데이터베이스에 삭제해주고 색깔은 회색리턴
            else:
                db.commentLike.delete_one({'comment_id':comment_id,'user_id':user_id})
                like_num = db.commentLike.count_documents({'comment_id':comment_id})
                return jsonify({'like_num': like_num, 'color':'grey'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/api/video/save', methods=['POST'])
@login_required
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
@login_required
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
        #댓글 카운팅해서 3개추출
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
        #list안에 dict형태로 담아서 json형식으로 리턴
        res = list(map(lambda item: {'_id': str(item["_id"]), 'content': item['content'], 'user_name': item['user_name'], 'thumbnail': item['thumbnail'], 'like_num': db.commentLike.count_documents({'comment_id': str(item["_id"])})}, rankers))
        return jsonify({'rankers': res})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
