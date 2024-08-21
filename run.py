from app import create_app
from app.init_db import insert_initial_data

app = create_app()

if __name__ == "__main__":
    
    with app.app_context():
        insert_initial_data()
        
    app.run(host='0.0.0.0', port=5000)