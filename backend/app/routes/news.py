from flask import Blueprint, request, jsonify
from backend.app.models.news import News
from backend.app.extensions import db

news_bp = Blueprint('news', __name__, url_prefix='/news')

@news_bp.route('/', methods=['GET'])
def get_news():
    """Отримати всі новини"""
    news_list = News.query.order_by(News.created_at.desc()).all()
    return jsonify([news.to_dict() for news in news_list]), 200

@news_bp.route('/<int:news_id>', methods=['GET'])
def get_news_item(news_id):
    """Отримати конкретну новину"""
    news = News.query.get_or_404(news_id)
    return jsonify(news.to_dict()), 200

@news_bp.route('/', methods=['POST'])
def create_news():
    """Створити новину"""
    data = request.get_json()
    new_news = News(title=data.get('title'), content=data.get('content'))
    db.session.add(new_news)
    db.session.commit()
    return jsonify(new_news.to_dict()), 201

@news_bp.route('/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    """Оновити новину"""
    news = News.query.get_or_404(news_id)
    data = request.get_json()
    news.title = data.get('title', news.title)
    news.content = data.get('content', news.content)
    db.session.commit()
    return jsonify(news.to_dict()), 200

@news_bp.route('/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    """Видалити новину"""
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    return jsonify({'message': 'News deleted successfully'}), 200
