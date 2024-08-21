from app import db

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Menu {self.name}>'
