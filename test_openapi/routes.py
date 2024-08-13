from flask import Blueprint, request, jsonify
import openai
from secrets import load_secrets

# 비밀정보 로드
secrets = load_secrets()

# OpenAI API 키 설정
openai.api_key = secrets.get('OPENAI_API_KEY')

# Blueprint 생성
api_bp = Blueprint('api', __name__)


@api_bp.route("/api/chat", methods=["POST"])
def chatbot():
    user_input = request.json.get("message")

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
