from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models import Service
from backend.app.extensions import db

services_bp = Blueprint('services', __name__, url_prefix='/services')


@services_bp.route('/', methods=['GET'])
def get_services():
    """Отримати всі сервіси"""
    try:
        services = Service.query.all()
        return jsonify([service.to_dict() for service in services]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Отримати інформацію про конкретний сервіс"""
    try:
        service = Service.query.get_or_404(service_id)
        return jsonify(service.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Service not found", "details": str(e)}), 404


@services_bp.route('/', methods=['POST'])
def create_service():
    """Створити новий сервіс"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing required field: 'name'"}), 400

    try:
        new_service = Service(name=data['name'], description=data.get('description'))
        db.session.add(new_service)
        db.session.commit()
        return jsonify(new_service.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


@services_bp.route('/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    """Оновити сервіс"""
    service = Service.query.get_or_404(service_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        for key, value in data.items():
            if hasattr(service, key):
                setattr(service, key, value)
        db.session.commit()
        return jsonify(service.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


@services_bp.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    """Видалити сервіс"""
    service = Service.query.get_or_404(service_id)
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
