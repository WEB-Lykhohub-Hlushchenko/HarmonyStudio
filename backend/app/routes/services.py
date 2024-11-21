from flask import Blueprint, request, jsonify
from backend.app.models import Service
from backend.app import db

services_bp = Blueprint('services', __name__, url_prefix='/services')

@services_bp.route('/', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services]), 200

@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify(service.to_dict()), 200

@services_bp.route('/', methods=['POST'])
def create_service():
    data = request.get_json()
    new_service = Service(**data)
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_dict()), 201

@services_bp.route('/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(service, key, value)
    db.session.commit()
    return jsonify(service.to_dict()), 200

@services_bp.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'}), 200
