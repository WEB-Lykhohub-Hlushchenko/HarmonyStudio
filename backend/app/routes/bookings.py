from flask import Blueprint, request, jsonify
from backend.app.models.user import User
from backend.app.models.master import Master
from backend.app.models.service import Service
from backend.app.models.booking import Booking
from backend.app.extensions import db
from sqlalchemy.exc import IntegrityError
import json

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
    print("Received booking data:", json.dumps(data, indent=4))  # Логування отриманих даних

    try:
        # Перевірка існування користувача та майстра
        user = User.query.get(data.get('user_id'))
        master = Master.query.get(data.get('master_id'))

        if not user or not master:
            return jsonify({"error": "Invalid user or master ID"}), 400

        # Автоматичне отримання service_id з майстра
        service_id = master.service_id

        # Створення нового бронювання
        new_booking = Booking(
            user_id=data.get('user_id'),
            master_id=data.get('master_id'),
            service_id=service_id,  # Визначаємо service_id автоматично
            booking_datetime=data.get('booking_datetime')
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



@bookings_bp.route('/client/<int:user_id>/appointments', methods=['GET'])
def get_client_appointments(user_id):
    """Отримати всі бронювання клієнта за user_id"""
    bookings = Booking.query.filter_by(user_id=user_id).all()

    appointments = []
    for booking in bookings:
        master = Master.query.get(booking.master_id)
        if master:
            user_data = User.query.get(master.user_id)  # Отримуємо дані майстра
            appointments.append({
                "id": booking.id,
                "master_name": f"{user_data.first_name} {user_data.last_name}",
                "booking_datetime": booking.booking_datetime.strftime("%Y-%m-%d %H:%M:%S")
            })

    return jsonify(appointments), 200
