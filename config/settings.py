from .secrets import load_secrets
import os

secrets = load_secrets()

# Clova API 키 설정
clova_api_key = secrets.get('CLOVA_API_KEY')

# TTS API 키
tts_api_key = secrets.get('TTS_API_KEY')

# TTS ID
tts_id = secrets.get('TTS_ID')

# 파일 저장 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
