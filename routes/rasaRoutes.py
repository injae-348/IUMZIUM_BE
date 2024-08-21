from flask import Blueprint, request, jsonify
from services.rasaService import send_message_to_rasa

rasa_bp = Blueprint('rasa', __name__)

@rasa_bp.route('/', methods=['GET','POST'])
def test():
    return 'test'

# RASA 서버로 바로 메시지 보내기 테스트
@rasa_bp.route('/test/', methods=['POST','OPTIONS'])
def send_message():
    if request.method == "OPTIONS":
        # OPTIONS 요청에 대한 응답
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    print('request: {}'.format(request))

    data = request.get_json()
    print('data: {}'.format(data))
    sender = data.get('sender')
    message = data.get('message')
    try:
        response = send_message_to_rasa(sender, message)
        print('response: {}'.format(response))
        return jsonify(response), 200
    except Exception as e:
        return jsonify([]), 500