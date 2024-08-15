import os
import requests
from pydub import AudioSegment


def download_audio(url, output_path):
    """URL에서 오디오 파일을 다운로드합니다."""
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except Exception as e:
        raise RuntimeError(f"Audio 다운로드 중 에러: {str(e)}")


def convert_to_m4a(input_path, output_path):
    """오디오 파일을 m4a 형식으로 변환합니다."""
    try:
        audio = AudioSegment.from_file(input_path)
        # 'm4a' 대신 'mp4' 또는 'ipod' 형식을 사용
        audio.export(output_path, format="mp4")  # 또는 format="ipod"
    except Exception as e:
        raise RuntimeError(f"Audio 변환 중 에러: {str(e)}")


def process_audio(audio_url):
    """URL에서 오디오를 다운로드하고 m4a 형식으로 변환합니다."""
    base_dir = os.path.dirname(__file__)
    temp_wav_path = os.path.join(base_dir, "temp_audio.wav")  # 임시 WAV 파일 경로
    output_m4a_path = os.path.join(base_dir, "temp_audio.m4a")  # 최종 m4a 파일 경로

    try:
        # 오디오 다운로드
        download_audio(audio_url, temp_wav_path)

        # m4a 형식으로 변환
        convert_to_m4a(temp_wav_path, output_m4a_path)

        return output_m4a_path  # 변환된 m4a 파일의 경로를 반환
    finally:
        # 임시 WAV 파일 삭제
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)


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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"Clova 번역 요청 에러": "Failed to process the audio file"}
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return {"Clova 번역 요청 모르는 에러": str(e)}
