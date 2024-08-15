from flask import Blueprint, request, jsonify
from services.chatService import handle_chat

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/", methods=["POST"])
def chatbot():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "'message' 필드가 필요합니다."}), 400

    response = handle_chat(user_input)
    return jsonify({"reply": response})
