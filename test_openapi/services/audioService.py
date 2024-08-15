import os
from pydub import AudioSegment
from config.settings import UPLOAD_FOLDER, clova_api_key
from utils.fileUtils import delete_files
from .clovaSpeech import transcribe_audio

def process_audio_file(audio_file):
    input_file_path = os.path.join(UPLOAD_FOLDER, 'temp_audio.wav')
    output_file_path = os.path.join(UPLOAD_FOLDER, 'temp_audio.m4a')
    audio_file.save(input_file_path)

    try:
        convert_to_m4a(input_file_path, output_file_path)
        return handle_audio_file(output_file_path, clova_api_key)
    except Exception as e:
        return {"error": str(e)}
    finally:
        delete_files([input_file_path, output_file_path])

def convert_to_m4a(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="mp4")

def handle_audio_file(output_file_path, clova_api_key):
    transcription_result = transcribe_audio(output_file_path, clova_api_key, 'Kor')
    if transcription_result and 'text' in transcription_result:
        return {"transcription": transcription_result['text']}
    else:
        return {"error": "Transcription failed"}
