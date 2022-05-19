from pymongo import MongoClient
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.classification


# 메인 페이지
@app.route('/')
def home():
    contents = db.contents.find()  # 전체 컨텐츠 데이터

    return render_template('index.html', contents=contents)
    # return jsonify({'message': 'success'})


# DB 자료 응답 (화면 구현용)
@app.route("/get_data", methods=["GET"])
def get_contents():
    contents = list(db.contents.find({}, {'_id': False}))

    return jsonify({'message': contents})


# 게시물 생성
@app.route("/content", methods=["POST"])
def content_post():
    file = request.files['file_give']  # 업로드한 이미지 파일
    image_receive = request.form['image_give']  # 업로드한 이미지명
    print(image_receive)
    ext = image_receive.split('.')[-1]  # 확장자 추출

    current_time = datetime.now()
    filename = f"{current_time.strftime('%Y%m%d%H%M%S')}.{ext}"
    save_to = f'static/img/post_contents/{filename}'  # 경로지정
    file.save(save_to)  # 이미지 파일 저장

    content_count = db.contents.find({}, {'_id': False}).collection.estimated_document_count()  # 전체 게시물 개수

    doc = {
        'post_id': content_count + 1,
        'img': image_receive,
        'f_name': filename,
    }
    db.contents.insert_one(doc)

    return jsonify({'msg': '게시물 생성 완료'})


@app.route('/content', methods=['GET'])
def content_list():
    photos = list(db.contents.find({}, {'_id': False}))
    return jsonify({'photos': photos})


# 게시물 타임스탬프
@app.route("/timestamp", methods=["GET"])
def timestamp_get():
    contents = list(db.data.find({}, {'_id': False}))

    timestamps = []
    for i in range(len(contents)):
        result = datetime.now() - (contents)[i]['timestamp']
        if 'day' in str(result):
            time = (str(result).split('d')[0] + '일 전')
        elif int(str(result).split(':')[0]) > 0:
            time = (str(result).split(':')[0] + '시간 전')
        else:
            time = (str(result).split(':')[1] + '분 전')
        timestamps.append({'post_id': i + 1, 'time': time})

    return jsonify({'timestamps': timestamps})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
