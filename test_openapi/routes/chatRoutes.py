from flask import Blueprint, request, jsonify
from services.chatService import handle_chat

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/", methods=["POST", "OPTIONS"])
def chatbot():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "'message' 필드가 필요합니다."}), 400

    response = handle_chat(user_input)
    return jsonify({"reply": response})