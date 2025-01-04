from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db
import os

def create_app():
    app = Flask(__name__)

    # Konfigurasi aplikasi
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')

    # Inisialisasi database
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)

    # Register blueprint
    from routes.auth import auth_bp
    from routes.books import books_bp
    from routes.orders import orders_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(orders_bp, url_prefix='/orders')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
