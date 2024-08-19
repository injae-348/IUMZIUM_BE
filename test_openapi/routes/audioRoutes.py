from flask import Blueprint, request, jsonify
from services.audioService import process_audio_file

audio_bp = Blueprint('audio', __name__)

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
    return jsonify(response)
