from flask import Blueprint, request, jsonify
from services.audioService import process_audio_file
from services.rasaService import send_message_to_rasa
from dto.RasaReqDto import RasaReqDto

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
    if transcription:
        user_message = RasaReqDto(sender = 'user', message = transcription)
        rasa_response = send_message_to_rasa(user_message)
        
        print("rasa_response: {}".format(rasa_response))
        return jsonify(rasa_response)
    else:
        return jsonify({"error": "음성 인식 실패"}), 500
