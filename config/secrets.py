import json
import os

BASE_URL = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_URL, '../secrets.json')

def load_secrets():
    with open(SECRET_FILE, 'r') as file:
        return json.load(file)
