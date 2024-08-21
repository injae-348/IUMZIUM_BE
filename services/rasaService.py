import requests

def send_message_to_rasa(rasa_req_dto):
    rasa_url = 'https://b2a4-124-53-16-60.ngrok-free.app/webhooks/rest/webhook'
    payload = {
        'sender': rasa_req_dto.sender,
        'message': rasa_req_dto.message
    }
    response = requests.post(rasa_url, json=payload)
    response.raise_for_status()
    return response.json()