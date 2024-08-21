import urllib.request
import urllib.parse
from config.settings import tts_api_key, tts_id

def text_to_speech(text, output_file="output.mp3"):
    """클로바 TTS API를 사용하여 텍스트를 음성으로 변환하고 MP3 파일로 저장합니다."""
    
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    data = {
        "speaker": "nara",   # 음성 종류를 선택합니다 (예: nara, jinho 등)
        "volume": "0",       # 볼륨 조절 (-5 ~ 5)
        "speed": "0",        # 속도 조절 (-5 ~ 5)
        "pitch": "0",        # 음 높이 조절 (-5 ~ 5)
        "format": "mp3",     # 출력 포맷
        "text": text         # 변환할 텍스트
    }
    
    encoded_data = urllib.parse.urlencode(data)
    
    request = urllib.request.Request(url, data=encoded_data.encode('utf-8'))
    request.add_header("X-NCP-APIGW-API-KEY-ID", tts_id)
    request.add_header("X-NCP-APIGW-API-KEY", tts_api_key)
    
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        
        if rescode == 200:
            print("TTS 변환 성공, 파일을 저장합니다.")
            with open(output_file, "wb") as f:
                f.write(response.read())
            print(f"파일이 {output_file}으로 저장되었습니다.")
        else:
            print(f"TTS API 요청 실패: 응답 코드 {rescode}")
    except Exception as e:
        print(f"예상치 못한 에러 발생: {str(e)}")

