from flask import Blueprint, request, jsonify
from backend.app.models.user import User
from backend.app.models.master import Master
from backend.app.models.service import Service
from backend.app.models.booking import Booking
from backend.app.extensions import db
from sqlalchemy.exc import IntegrityError

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bookings_bp.route('/', methods=['GET'])
def get_bookings():
    """Отримати список усіх бронювань"""
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@bookings_bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Отримати інформацію про конкретне бронювання"""
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict()), 200

@bookings_bp.route('/', methods=['POST'])
def create_booking():
    """Створити нове бронювання"""
    data = request.get_json()

    try:
        # Перевірка існування користувача, майстра та послуги
        user = User.query.get(data.get('user_id'))
        master = Master.query.get(data.get('master_id'))
        service = Service.query.get(data.get('service_id'))

        if not user or not master or not service:
            return jsonify({"error": "Invalid user, master, or service ID"}), 400

        # Створення нового бронювання
        new_booking = Booking(
            user_id=data.get('user_id'),
            master_id=data.get('master_id'),
            service_id=data.get('service_id'),
            booking_datetime=data.get('booking_datetime'),
            status=data.get('status')
        )

        db.session.add(new_booking)
        db.session.commit()
        return jsonify(new_booking.to_dict()), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """Оновити бронювання"""
    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json()

    # Оновлення полів бронювання
    for key, value in data.items():
        if hasattr(booking, key):
            setattr(booking, key, value)

    db.session.commit()
    return jsonify(booking.to_dict()), 200

@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """Видалити бронювання"""
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted successfully'}), 200
