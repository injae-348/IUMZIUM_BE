from flask import jsonify
import os
import requests
from pydub import AudioSegment


def handle_audio_file(output_file_path, clova_api_key):
    """파일을 받아서 텍스트로 변환한 후 결과를 반환합니다."""
    try:
        # Clova Speech API를 사용하여 음성 파일을 텍스트로 변환
        transcription_result = transcribe_audio(
            output_file_path, clova_api_key, 'Kor')

        # 결과 처리 및 파일 삭제
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        if transcription_result and 'text' in transcription_result:
            return jsonify({"transcription": transcription_result['text']})
        else:
            return jsonify({"출력 결과 에러": "Transcription failed"}), 500
    except Exception as e:
        return jsonify({"모든 에러": str(e)}), 500

def convert_to_m4a(input_path, output_path):
    """오디오 파일을 m4a 형식으로 변환합니다."""
    try:
        audio = AudioSegment.from_file(input_path)
        # 'm4a' 대신 'mp4' 또는 'ipod' 형식을 사용
        audio.export(output_path, format="mp4")  # 또는 format="ipod"
    except Exception as e:
        raise RuntimeError(f"Audio 변환 중 에러: {str(e)}")


def transcribe_audio(file_path, api_key, lang='Kor'):
    """Clova Speech API를 사용하여 음성 파일을 텍스트로 변환합니다."""
    url = "https://clovaspeech-gw.ncloud.com/recog/v1/stt"
    headers = {
        "X-CLOVASPEECH-API-KEY": api_key,
        "Content-Type": "application/octet-stream"
    }
    params = {
        "lang": lang
    }

    try:
        with open(file_path, 'rb') as audio_file:
            response = requests.post(
                url, headers=headers, params=params, data=audio_file)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패: {e}")
        print(f"응답 내용: {response.text}")  # 응답 내용을 로그에 출력
        return {"Clova 번역 요청 에러": "Failed to process the audio file"}
    except Exception as e:
        print(f"예상치 못한 에러 발생: {str(e)}")
        return {"Clova 번역 요청 모르는 에러": str(e)}