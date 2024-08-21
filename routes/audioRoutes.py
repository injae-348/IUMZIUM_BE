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

    # Rasa 응답 + TTS로 변환시켜 (text & tts)FE 반환
    if transcription:
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
    else:
        return jsonify({"error": "음성 인식 실패"}), 500