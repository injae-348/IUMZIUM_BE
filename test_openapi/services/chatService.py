import openai
from config.settings import openai_api_key

openai.api_key = openai_api_key

def handle_chat(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in providing financial advice."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message['content']
