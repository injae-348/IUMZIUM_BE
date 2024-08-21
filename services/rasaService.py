import requests

def send_message_to_rasa(sender, message):
    print("sender: {}".format(sender))
    print("message: {}".format(message))
    rasa_url = 'https://c013-36-38-187-106.ngrok-free.app/webhooks/rest/webhook'
    # rasa_url = 'http://192.168.0.122:5005/webhooks/rest/webhook'

    payload = {
        'sender': sender,
        'message': message
    }
    response = requests.post(rasa_url, json=payload)
    print("rasa server response: {}".format(response))
    response.raise_for_status()
    return response.json()