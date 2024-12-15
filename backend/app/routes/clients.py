from flask import Blueprint, request, jsonify
from backend.app.models.client import Client
from backend.app.models.booking import Booking
from backend.app.extensions import db
from sqlalchemy.exc import IntegrityError

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')


@clients_bp.route('/', methods=['GET'])
def get_clients():
    """Отримати список усіх клієнтів"""
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients]), 200


@clients_bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Отримати інформацію про конкретного клієнта разом із записами"""
    client = Client.query.get_or_404(client_id)
    response = client.to_dict()

    # Додаємо записи клієнта (якщо є)
    bookings = Booking.query.filter_by(user_id=client.id).all()
    response['appointments'] = [
        {
            "id": booking.id,
            "master_id": booking.master_id,
            "service_id": booking.service_id,
            "booking_datetime": booking.booking_datetime
        }
        for booking in bookings
    ]

    return jsonify(response), 200


@clients_bp.route('/', methods=['POST'])
def create_client():
    """Створити нового клієнта"""
    data = request.get_json()

    # Вибір дозволених полів
    allowed_fields = ['id', 'additional_info']
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}

    try:
        new_client = Client(**filtered_data)
        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Client with this ID already exists"}), 400


@clients_bp.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Оновити інформацію про клієнта"""
    client = Client.query.get_or_404(client_id)
    data = request.get_json()

    # Оновлюємо тільки дозволені поля
    allowed_fields = ['additional_info']
    for key, value in data.items():
        if key in allowed_fields and hasattr(client, key):
            setattr(client, key, value)

    db.session.commit()
    return jsonify(client.to_dict()), 200


@clients_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Видалити клієнта"""
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted successfully'}), 200

@clients_bp.route('/<int:client_id>/appointments', methods=['GET'])
def get_client_appointments(client_id):
    """Отримати всі записи клієнта за ID"""
    client = Client.query.get_or_404(client_id)
    bookings = Booking.query.filter_by(user_id=client.id).all()

    return jsonify([
        {
            "id": booking.id,
            "master_id": booking.master_id,
            "service_id": booking.service_id,
            "booking_datetime": booking.booking_datetime
        }
        for booking in bookings
    ]), 200
