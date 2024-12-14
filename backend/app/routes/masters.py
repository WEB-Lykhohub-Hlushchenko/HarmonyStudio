from flask import Blueprint, request, jsonify
from backend.app.models.master import Master  # Використовуємо модель Master
from backend.app.extensions import db
from sqlalchemy.exc import IntegrityError

masters_bp = Blueprint('masters', __name__, url_prefix='/masters')

@masters_bp.route('/', methods=['GET'])
def get_masters():
    """Отримати список усіх майстрів"""
    masters = Master.query.all()
    return jsonify([master.to_dict() for master in masters]), 200

@masters_bp.route('/<int:master_id>', methods=['GET'])
def get_master(master_id):
    """Отримати інформацію про конкретного майстра"""
    master = Master.query.get_or_404(master_id)
    return jsonify(master.to_dict()), 200

@masters_bp.route('/', methods=['POST'])
def create_master():
    """Створити нового майстра"""
    data = request.get_json()
    try:
        new_master = Master(
            user_id=data.get('user_id'),
            service_id=data.get('service_id'),
            bio=data.get('bio')
        )
        db.session.add(new_master)
        db.session.commit()
        return jsonify(new_master.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@masters_bp.route('/<int:master_id>', methods=['PUT'])
def update_master(master_id):
    """Оновити інформацію про майстра"""
    master = Master.query.get_or_404(master_id)
    data = request.get_json()
    for key, value in data.items():
        if hasattr(master, key):
            setattr(master, key, value)
    db.session.commit()
    return jsonify(master.to_dict()), 200

@masters_bp.route('/<int:master_id>', methods=['DELETE'])
def delete_master(master_id):
    """Видалити майстра"""
    master = Master.query.get_or_404(master_id)
    db.session.delete(master)
    db.session.commit()
    return jsonify({'message': 'Master deleted successfully'}), 200