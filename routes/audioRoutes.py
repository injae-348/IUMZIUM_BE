from flask import Blueprint, request, jsonify, Response
from werkzeug.wsgi import wrap_file
from services.audioService import process_audio_file
from services.rasaService import send_message_to_rasa
from services.ttsService import text_to_speech
from dto.RasaReqDto import RasaReqDto
from werkzeug.http import HTTP_STATUS_CODES
from utils.fileUtils import delete_files
import uuid
import os
import io
import tempfile
import requests

audio_bp = Blueprint('audio', __name__)

# 클로바 API만 호출 -> 텍스트 응답
# response: {'transcription': '안녕하세요'}
@audio_bp.route("/", methods=["POST", "OPTIONS"])
def audiobot():
    if request.method == "OPTIONS":
        # OPTIONS 요청에 대한 응답
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    if 'file' not in request.files:
        return jsonify({"error": "파일이 포함되지 않았습니다."}), 400

    audio_file = request.files['file']
    response = process_audio_file(audio_file)

    print("response: {}".format(response))

    return jsonify(response)

@audio_bp.route("/greet/", methods=["POST", "OPTIONS"])
def sayHello():
    if request.method == "OPTIONS":
        # OPTIONS 요청에 대한 응답
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    # 텍스트와 음성 파일 생성
    greeting_text = "안녕하세요! 무엇을 도와드릴까요?"
    
    # 텍스트를 음성 파일로 변환
    greet_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
    text_to_speech(greeting_text, greet_audio_file)

    # Multipart 응답 생성
    def generate():
        try:
            # 텍스트 부분
            yield '--boundary\r\n'
            yield 'Content-Disposition: form-data; name="text"\r\n'
            yield 'Content-Type: text/plain\r\n\r\n'
            yield (greeting_text + '\r\n').encode('utf-8')
            yield '\r\n'

            # 음성 파일 부분
            with open(greet_audio_file, 'rb') as audio_file:
                audio_data = audio_file.read()
            yield '--boundary\r\n'
            yield 'Content-Disposition: form-data; name="audio"; filename="greeting.mp3"\r\n'
            yield 'Content-Type: audio/mpeg\r\n\r\n'
            yield audio_data
            yield '\r\n'

            yield '--boundary--'
        finally:
            # 파일 삭제
            if os.path.exists(greet_audio_file):
                os.remove(greet_audio_file)

    response = Response(generate(), content_type='multipart/form-data; boundary=boundary')

    return response


# 클로바 API + Rasa 서버 호출
@audio_bp.route("/rasa/", methods=["POST", "OPTIONS"])
def audioRasa():
    if request.method == "OPTIONS":
        # OPTIONS 요청에 대한 응답
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    if 'file' not in request.files:
        return jsonify({"error": "파일이 포함되지 않았습니다."}), 400

    audio_file = request.files['file']
    clova_response = process_audio_file(audio_file)
    print("clova_response: {}".format(clova_response))

    transcription = clova_response.get('transcription')
    print("transcription: {}".format(transcription))

    # Rasa 응답 + TTS로 변환시켜 (text & tts)FE 반환
    if transcription:
        category = None
        category_text = None

        if (("차" in transcription or "자" in transcription) and "목록" in transcription):
            category = "tea"
            category_text = "차 목록을 보여줍니다"
        elif "커피" in transcription and "목록" in transcription:
            category = "coffee"
            category_text = "커피 목록을 보여줍니다"
        elif (("에이드" in transcription or "레이드" in transcription) and "목록" in transcription):
            category = "ade"
            category_text = "에이드 목록을 보여줍니다"
        elif "디카페인" in transcription and "목록" in transcription:
            category = "decaf"
            category_text = "디카페인 목록을 보여줍니다."


        if category:
            # 카테고리 텍스트를 음성 파일로 생성
            category_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
            text_to_speech(category_text, category_audio_file)

            # API 호출 URL 생성 -> https로 변경
            api_url = f"https://52.78.120.182.nip.io/api/drink?category={category}"
            # api_url = f"{request.url_root}/api/drink?category={category}"
            print('api_url: {}'.format(api_url))
            # Multipart 응답 생성
            def generate():
                try:
                    # 카테고리 텍스트 음성 파일 부분
                    with open(category_audio_file, 'rb') as audio_file:
                        audio_data = audio_file.read()
                    yield '--boundary\r\n'
                    yield 'Content-Disposition: form-data; name="category_audio"; filename="category_text.mp3"\r\n'
                    yield 'Content-Type: audio/mpeg\r\n\r\n'
                    yield audio_data
                    yield '\r\n'

                    # 카테고리 텍스트 부분
                    yield '--boundary\r\n'
                    yield 'Content-Disposition: form-data; name="category_text"\r\n'
                    yield 'Content-Type: text/plain\r\n\r\n'
                    yield category_text.encode('utf-8')
                    yield '\r\n'

                    # API 주소 부분
                    yield '--boundary\r\n'
                    yield 'Content-Disposition: form-data; name="api_url"\r\n'
                    yield 'Content-Type: text/plain\r\n\r\n'
                    yield api_url.encode('utf-8')
                    yield '\r\n'

                    yield '--boundary--'
                finally:
                    # 파일 삭제
                    if os.path.exists(category_audio_file):
                        os.remove(category_audio_file)

            response = Response(generate(), content_type='multipart/form-data; boundary=boundary')

            return response
               
        else:
            rasa_response = send_message_to_rasa('user',transcription)
            print("rasa_response: {}".format(rasa_response))

            # MP3 파일 경로를 저장할 리스트
            mp3_files = []

            # 멀티파트 응답을 생성하기 위한 제너레이터 함수
            def generate():
                for idx, message in enumerate(rasa_response):
                    text_response = message.get('text', f'기본 응답 메시지 {idx + 1}')
                    
                    # 임시 파일 생성 (플랫폼에 관계없이 올바른 경로 생성)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3:
                        output_file = temp_mp3.name
                    mp3_files.append(output_file)

                    # 텍스트를 음성으로 변환
                    text_to_speech(text_response, output_file)

                    # MP3 파일을 읽기 위한 파일 객체 생성
                    with open(output_file, 'rb') as mp3_file:
                        mp3_data = mp3_file.read()

                    # 텍스트 부분 생성
                    yield '--boundary\r\n'
                    yield f'Content-Disposition: form-data; name="text{idx+1}"\r\n\r\n'
                    yield f'{text_response}\r\n'

                    # MP3 파일 부분 생성
                    yield '--boundary\r\n'
                    yield f'Content-Disposition: form-data; name="audio{idx+1}"; filename="response{idx+1}.mp3"\r\n'
                    yield 'Content-Type: audio/mpeg\r\n\r\n'
                    yield mp3_data
                    yield '\r\n'

                yield '--boundary--'

            # 응답 객체 생성
            response = Response(generate(), content_type='multipart/form-data; boundary=boundary')
            print("multi part response: {}".format(response))
            # 응답 반환 후 파일 삭제
            try:
                return response
            finally:
                # 생성된 모든 MP3 파일 삭제
                for file in mp3_files:
                    try:
                        os.remove(file)
                        print(f"파일 {file} 삭제 완료.")
                    except Exception as e:
                        print(f"파일 삭제 중 오류 발생: {e}")


def get_category_and_text(transcription):
    # 카테고리와 텍스트 정보를 담을 리스트
    categories = [
        {"keywords": ["차"], "text": "차 목록을 보여줍니다", "category": "tea"},
        {"keywords": ["커피"], "text": "커피 목록을 보여줍니다", "category": "coffee"},
        {"keywords": ["에이드", "레이드"], "text": "에이드 목록을 보여줍니다", "category": "ade"},
        {"keywords": ["디카페인"], "text": "디카페인 목록을 보여줍니다.", "category": "decaf"}
    ]
    
    for item in categories:
        # 각 항목의 키워드와 목록을 확인
        if all(keyword in transcription for keyword in item["keywords"]) and "목록" in transcription:
            return item["category"], item["text"]
    
    # 조건에 맞는 항목이 없을 경우 None 반환
    return None, None