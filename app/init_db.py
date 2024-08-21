from app import db
from app.models import Menu

def insert_initial_data():
    db.create_all()  # 테이블 생성

    # 기본 데이터 삽입
    if not Menu.query.first():  # 테이블이 비어있다면 데이터 삽입
        initial_data = [
            {'name': '아메리카노', 'price': 4000, 'category': 'coffee', 'image_name': 'americano.png'},
            {'name': '카페라떼', 'price': 4500, 'category': 'coffee', 'image_name': 'caffelatte.png'},
            {'name': '연유라떼', 'price': 5000, 'category': 'coffee', 'image_name': 'condensedmilk_latte.png'},
            {'name': '바닐라라떼', 'price': 4800, 'category': 'coffee', 'image_name': 'vanilla_latte.png'},
            {'name': '카푸치노', 'price': 4500, 'category': 'coffee', 'image_name': 'cappuccino.png'},
            {'name': '카라멜마끼야또', 'price': 5000, 'category': 'coffee', 'image_name': 'caramel_macchiato.png'},
            {'name': '카페모카', 'price': 4700, 'category': 'coffee', 'image_name': 'caffe_mocha.png'},
            {'name': '아인슈페너', 'price': 5500, 'category': 'coffee', 'image_name': 'eiskaffee.png'},
            {'name': '복숭아티', 'price': 3500, 'category': 'tea', 'image_name': 'peach_tea.png'},
            {'name': '리치캐모마일', 'price': 4000, 'category': 'tea', 'image_name': 'lychee_camomile.png'},
            {'name': '청귤얼그레이', 'price': 3800, 'category': 'tea', 'image_name': 'green_citrus_earlgrey.png'},
            {'name': '트리플민트', 'price': 3600, 'category': 'tea', 'image_name': 'triple_mint.png'},
            {'name': '애플히비스커스', 'price': 3700, 'category': 'tea', 'image_name': 'apple_hibiscus.png'},
            {'name': '허나유자티', 'price': 3900, 'category': 'tea', 'image_name': 'honey_yuja_tea.png'},
            {'name': '허니자몽티', 'price': 4000, 'category': 'tea', 'image_name': 'honey_persimmon_tea.png'},
            {'name': '허니레몬티', 'price': 3800, 'category': 'tea', 'image_name': 'honey_lemon_tea.png'},
            {'name': '레몬 에이드', 'price': 4000, 'category': 'ade', 'image_name': 'lemonade.png'},
            {'name': '망고 에이드', 'price': 4000, 'category': 'ade', 'image_name': 'mangoade.png'},
            {'name': '하비스커스 에이드', 'price': 4200, 'category': 'ade', 'image_name': 'hibiscus_aid.png'},
            {'name': '블루베리 에이드', 'price': 4500, 'category': 'ade', 'image_name': 'blueberry_aid.png'},
            {'name': '자몽에이드', 'price': 4300, 'category': 'ade', 'image_name': 'grapefruit_aid.png'},
            {'name': '디카페인 아메리카노', 'price': 4000, 'category': 'decaf', 'image_name': 'decaffein_americano.png'},
            {'name': '디카페인 카페라떼', 'price': 4500, 'category': 'decaf', 'image_name': 'decaffein_caffelatte.png'},
            {'name': '디카페인 연유라떼', 'price': 5000, 'category': 'decaf', 'image_name': 'decaffein_condensedmilk_latte.png'},
            {'name': '디카페인 바닐라라떼', 'price': 4800, 'category': 'decaf', 'image_name': 'decaffein_vanilla_latte.png'},
            {'name': '디카페인 카푸치노', 'price': 4500, 'category': 'decaf', 'image_name': 'decaffein_cappuccino.png'},
            {'name': '디카페인 마끼야또', 'price': 5000, 'category': 'decaf', 'image_name': 'decaffein_caramel_macchiato.png'},
            {'name': '디카페인 카페모카', 'price': 4700, 'category': 'decaf', 'image_name': 'decaffein_caffe_mocha.png'},
            {'name': '디카페인 아인슈페너', 'price': 5500, 'category': 'decaf', 'image_name': 'decaffein_eiskaffee.png'}
        ]       

        for item in initial_data:
            menu_item = Menu(name=item['name'], price=item['price'], category=item['category'], image_name=item['image_name'])
            db.session.add(menu_item)
        db.session.commit()
