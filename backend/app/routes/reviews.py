from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models import Review, Master, User
from backend.app.extensions import db

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# === Функції для клієнтів ===
@reviews_bp.route('/master/<int:master_id>', methods=['GET'])
def get_reviews_for_master(master_id):
    """Отримати всі відгуки для майстра"""
    try:
        reviews = Review.query.filter_by(master_id=master_id).all()
        return jsonify([review.to_dict() for review in reviews]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

@reviews_bp.route('/master/<int:master_id>', methods=['POST'])
def add_review_for_master(master_id):
    """Додати відгук для майстра"""
    data = request.get_json()
    try:
        new_review = Review(
            master_id=master_id,
            client_id=data.get('client_id'),
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

# === CRUD для адмінпанелі ===
@reviews_bp.route('/', methods=['GET'])
def get_all_reviews():
    """Отримати всі відгуки (для адмінпанелі)"""
    try:
        reviews = Review.query.all()
        return jsonify([review.to_dict() for review in reviews]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """Оновити відгук (для адмінпанелі)"""
    review = Review.query.get_or_404(review_id)
    data = request.get_json()
    try:
        for key, value in data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        db.session.commit()
        return jsonify(review.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Видалити відгук"""
    review = Review.query.get_or_404(review_id)
    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Review deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
