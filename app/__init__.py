from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Підключення конфігурації
    db.init_app(app)  # Ініціалізація SQLAlchemy
    migrate.init_app(app, db)  # Ініціалізація Flask-Migrate

    # Імпорт маршруту після ініціалізації db
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Імпорт моделей після ініціалізації db (щоб уникнути циклічних імпортів)
    with app.app_context():
        from app import models
        print(models.User)  # Перевірка, чи імпортується модель

    return app
