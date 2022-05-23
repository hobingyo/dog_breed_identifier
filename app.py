from pymongo import MongoClient
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
import tensorflow as tf
import numpy as np


app = Flask(__name__)

client = MongoClient('mongodb+srv://******@cluster0.*******.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.*****


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
    username_receive = request.form['username_give']
    print(image_receive)
    ext = image_receive.split('.')[-1]  # 확장자 추출

    current_time = datetime.now()
    filename = f"{current_time.strftime('%Y%m%d%H%M%S')}.{ext}"
    save_to = f'static/img/post_contents/{filename}'  # 경로지정
    file.save(save_to)  # 이미지 파일 저장

    content_count = db.contents.find(
        {}, {'_id': False}).collection.estimated_document_count()  # 전체 게시물 개수

    model = tf.keras.models.load_model('static/model/model.h5')
    test_url = f'static/img/post_contents/{filename}'
    test_generator = tf.keras.preprocessing.image.load_img(test_url, grayscale=False, color_mode="rgb",
                                                           target_size=(299, 299))
    input_arr = tf.keras.preprocessing.image.img_to_array(test_generator)
    input_arr = np.array([input_arr])
    input_arr /= 225.

    pred = model.predict(input_arr)
    pred2 = pred.argmax(axis=-1)
    dog_list = ['아펜핀셔', '아프간하운드', '에어데일 테리어', '아키타견', '알래스칸 맬러뮤트', '아메리칸 에스키모', '아메리칸 폭스하운드', '아메리칸 스태퍼드셔 테리어',
                '아메리칸 워터 스패니얼', '아나톨리아 셰퍼드', '오스트레일리안 캐틀독', '오스트레일리언 셰퍼드', '오스트레일리안 테리어', '바센지', '바셋하운드', '비글',
                '비어디드 콜리',
                '보스롱', '베들링턴 테리어', '벨지안 셰퍼드', '벨지안 셰퍼드', '벨기에 테뷰런', '버니즈 마운틴 도그', '비숑 프리제', '블랙 앤 탄 쿤하운드', '블랙 러시안 테리어',
                '블러드 하운드', '블루틱 쿤하운드', '보더콜리', '보더 테리어', '보르조이', '보스턴 테리어', '부비에 데 플랑드르', '복서', '보이킨 스파니엘', '브리아드',
                '브리타니',
                '브뤼셀 그리폰', '불테리어', '불독', '불마스티프', '케언 테리어', '가나안 도그', '케인 코르소', '카디건 웰시코기', '카발리에 킹 찰스 스패니얼',
                '체서피크 베이 리트리버', '치와와', '차이니스 크레스티드', '샤페이', '차우차우', '클럼버 스파니엘', '코커 스패니얼', '콜리', '컬리 코티드 리트리버', '닥스훈트',
                '달마티안', '댄디 딘몬트 테리어', '도베르만 핀셔', '도그 드 보르도', '잉글리쉬 코카스파니엘', '잉글리쉬 세터', '잉글리쉬 스프링거 스파니엘', '잉글리시 토이 스파니엘',
                '엔틀부처 제넨훈트', '필드 스파니엘', '피니시 스피츠', '플랫 코티드 리트리버', '프렌치 불독', '저먼 핀셔', '저먼 셰퍼드', '저먼 숏헤어드 포인터',
                '저먼 와이어헤어드 포인터', '자이언트 슈나우저', '글랜 오브 이말 테리어', '골든 리트리버', '고든 세터', '그레이트 데인', '그레이트 피레네',
                '그레이트 스위스 마운틴 독',
                '그레이 하운드', '허베너스', '이비잔 하운드', '아이슬란딕 쉽 독', '아이리시 레드 엔 화이트 세터', '아이리시 세터', '아이리시 테리어', '아이리시 워터 스파니엘',
                '아이리시 울프하운드', '이탈리안 그레이 하운드', '재패니즈친', '케이스혼트', '케리 블루 테리어', '코몬돌', '쿠바츠', '래브라도 리트리버', '레이클랜드 테리어',
                '레온베르거', '라사압소', '로첸', '말티즈', '맨체스터 테리어', '잉글리쉬 마스티프', '미니어처 슈나우져', '나폴리탄 마스티프', '뉴펀들랜드', '놀퍽 테리어',
                '노르웨이안 부훈트', '노르웨이안 엘크하운드', '노르웨이안 런드헌드', '노리치 테리어', '노바 스코셔 덕 톨링 레트리버', '올드 잉글리쉬 쉽독', '오터하운드', '파필리온',
                '파슨러쉘테리어', '페키니즈', '펨브로크 웰시코기', '페팃 바셋 그리폰 벤딘', '파라오 하운드', '플롯', '포인터', '포메라니안', '푸들', '포르투갈 워터 독',
                '세인트 베나드', '실크테리어', '스무스 폭스 테리어', '티벳 마스티프', '웰시 스프링거 스파니엘', '와이어헤어 포인팅 그리폰', '멕시칸 헤어리스 도그', '요크셔테리어']
    dog_name = dog_list[pred2[0]]
    print(dog_name)

    doc = {
        'post_id': content_count + 1,
        'username': username_receive,
        'img': image_receive,
        'f_name': filename,
        'dog_name': dog_name
    }
    print(doc)
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

# # 게시물 삭제
# @app.route("/content", methods=["POST"])
# def content_delete():
#     db.contents.remove({_id,})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
