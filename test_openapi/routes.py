from flask import Blueprint, request, jsonify
import openai
from secrets import load_secrets
from audio import handle_audio_file, convert_to_m4a
import os
import requests

# secret Key Load
secrets = load_secrets()

# OpenAI API 키 설정
openai.api_key = secrets.get('OPENAI_API_KEY')

# Clova API 키 설정
clova_api_key = secrets.get('CLOVA_API_KEY')

# 파일 저장 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Blueprint 생성
api_bp = Blueprint('api', __name__)


@api_bp.route("/api/chat", methods=["POST"])
def chatbot():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "'message' 필드가 필요합니다."}), 400

    # GPT-4 모델 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 최신 모델 이름 사용
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in providing financial advice."},
            {"role": "user", "content": user_input}
        ]
    )

    # GPT-4의 응답 추출
    bot_reply = response.choices[0].message['content']
    return jsonify({"reply": bot_reply})


@api_bp.route("/api/audio", methods=["POST"])
def audiobot():
    if 'file' not in request.files:
        return jsonify({"error": "파일이 포함되지 않았습니다."}), 400

    audio_file = request.files['file']
    input_file_path = os.path.join(UPLOAD_FOLDER, 'temp_audio.wav')
    output_file_path = os.path.join(UPLOAD_FOLDER, 'temp_audio.m4a')
    audio_file.save(input_file_path)

    try:
        # mp3 파일을 m4a로 변환
        convert_to_m4a(input_file_path, output_file_path)
        return handle_audio_file(output_file_path, clova_api_key)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(input_file_path):
            os.remove(input_file_path)
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
