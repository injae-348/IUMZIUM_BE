from flask import Blueprint, request, jsonify
from services.rasaService import send_message_to_rasa

rasa_bp = Blueprint('rasa', __name__)

# RASA 서버로 바로 메시지 보내기 테스트
@rasa_bp.route('/send/', methods=['POST','OPTIONS'])
def send_message():
    if request.method == "OPTIONS":
        # OPTIONS 요청에 대한 응답
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    data = request.get_json()
    sender = data.get('sender')
    message = data.get('message')
    try:
        response = send_message_to_rasa(sender, message)
        return jsonify(response), 200
    except Exception as e:
        return jsonify([]), 500