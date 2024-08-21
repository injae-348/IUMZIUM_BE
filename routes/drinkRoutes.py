from flask import Blueprint, request, jsonify, url_for
from app.models import Menu

drink_bp = Blueprint('drink', __name__)

VALID_CATEGORIES = {"tea", "coffee", "ade", "decaf"}

@drink_bp.route('/', methods=['GET'])
def get_drinks_by_category():
    # if request.method == "OPTIONS":
    #     # OPTIONS 요청에 대한 응답
    #     response = jsonify({})
    #     response.headers.add("Access-Control-Allow-Origin", "*")
    #     response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    #     response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    #     return response
    
    category = request.args.get('category', default=None, type=str)

    if category is None:
        return jsonify({"error": "Category 는 필수입니다."}), 400

    if category not in VALID_CATEGORIES:
        return jsonify({"error": "적절하지 않은 카테고리 입니다. 다음 중 하나를 입력 해주세요 : 차, 커피, 에이드."}), 400

    drinks = Menu.query.filter_by(category=category).all()

    if not drinks:
        return jsonify({"message": "해당 하는 카테고리는 존재하지 않습니다."}), 404

    base_url = url_for('static', filename='img/', _external=True)
    print('baseURL={}'.format(base_url))

    drinks_list = [{
        'name': drink.name,
        'price': drink.price,
        'category': drink.category,
        'image_path': f"{base_url}{drink.image_name}"
    } for drink in drinks]

    return jsonify(drinks_list)