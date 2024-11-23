from flask import Flask
from backend.config import Config
from backend.app.extensions import db, migrate
from backend.app.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    # Реєстрація маршрутів
    register_routes(app)

    # Імпортуємо моделі для доступності у міграціях
    with app.app_context():
        from backend.app.models import user, service, master, booking

    return app
