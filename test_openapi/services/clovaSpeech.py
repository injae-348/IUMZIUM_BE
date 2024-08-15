import requests

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
        return {"error": "Failed to process the audio file"}
    except Exception as e:
        print(f"예상치 못한 에러 발생: {str(e)}")
        return {"error": str(e)}
