from flask import Blueprint, request, jsonify
import openai
from secrets import load_secrets
from audio import transcribe_audio, process_audio
import os
import requests

# 비밀정보 로드
secrets = load_secrets()

# OpenAI API 키 설정
openai.api_key = secrets.get('OPENAI_API_KEY')

# Clova API 키 설정
clova_api_key = secrets.get('CLOVA_API_KEY')

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
    # 프론트엔드에서 전달된 URL과 언어를 받아옵니다.
    audio_url = request.json.get("audio_url")
    lang = request.json.get("lang", "Kor")  # 언어 설정, 기본값은 'Kor'

    if not audio_url:
        return jsonify({"error": "제공된 URL이 없습니다."}), 400

    try:
        # 음성 파일을 다운로드하고 m4a 형식으로 변환
        output_file_path = process_audio(audio_url)

        # Clova Speech API를 사용하여 음성 파일을 텍스트로 변환
        transcription_result = transcribe_audio(
            output_file_path, clova_api_key, lang)

        # 결과 처리 및 파일 삭제
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        if transcription_result and 'text' in transcription_result:
            return jsonify({"transcription": transcription_result['text']})
        else:
            return jsonify({"출력 결과 에러": "Transcription failed"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"오디오 파일 처리중 에러": "Failed to process the audio file"}), 500

    except Exception as e:
        return jsonify({"모든 에러": str(e)}), 500
