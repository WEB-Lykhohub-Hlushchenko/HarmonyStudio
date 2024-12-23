from .services import services_bp
from .auth import auth_bp
from .bookings import bookings_bp
from .faq import faq_bp
from .masters import masters_bp
from .clients import clients_bp
from .news import news_bp
from .reviews import reviews_bp
from .users import users_bp

def register_routes(app):
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(faq_bp, url_prefix='/faq')
    app.register_blueprint(masters_bp, url_prefix='/masters')
    app.register_blueprint(bookings_bp, url_prefix='/bookings')
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(news_bp,  url_prefix='/news')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(users_bp, url_prefix='/users')

