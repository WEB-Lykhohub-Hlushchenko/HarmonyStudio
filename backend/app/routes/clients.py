from flask import Blueprint, request, jsonify
from backend.app.models.client import Client
from backend.app.extensions import db
from sqlalchemy.exc import IntegrityError

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients]), 200

@clients_bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client.to_dict()), 200

@clients_bp.route('/', methods=['POST'])
def create_client():
    data = request.get_json()
    try:
        new_client = Client(**data)
        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Client with this email already exists"}), 400

@clients_bp.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    for key, value in data.items():
        if hasattr(client, key):
            setattr(client, key, value)
    db.session.commit()
    return jsonify(client.to_dict()), 200

@clients_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted successfully'}), 200
