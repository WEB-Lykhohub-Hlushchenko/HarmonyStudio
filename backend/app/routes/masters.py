from flask import Blueprint, request, jsonify
from backend.app.models.master import Master
from backend.app.models.user import User  # Імпортуємо модель User
from backend.app.extensions import db
from sqlalchemy.exc import IntegrityError
from backend.app.models.booking import Booking
from backend.app.models.service import Service


masters_bp = Blueprint('masters', __name__, url_prefix='/masters')

@masters_bp.route('/', methods=['GET'])
def get_masters():
    """Отримати список усіх майстрів"""
    masters = Master.query.all()
    return jsonify([master.to_dict() for master in masters]), 200


@masters_bp.route('/<int:user_id>', methods=['GET'])
def get_master(user_id):
    """Отримати інформацію про конкретного майстра разом із даними користувача"""
    # Знаходимо майстра за user_id
    master = Master.query.filter_by(user_id=user_id).first()

    # Якщо майстра не знайдено
    if not master:
        return jsonify({"error": "Master not found"}), 404

    # Отримуємо дані користувача через Foreign Key
    user_data = User.query.get_or_404(master.user_id)

    # Формуємо відповідь
    response = {
        "master_id": master.id,  # ID майстра
        "service_id": master.service_id,  # Безпосередньо ID сервісу, який присвоєний майстру
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "email": user_data.email,
        "phone_number": user_data.phone_number,
        "bio": master.bio or "No bio available"
    }

    return jsonify(response), 200





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

@masters_bp.route('/<int:master_id>/bio', methods=['PUT'])
def update_master_bio(master_id):
    """Оновити біографію майстра"""
    master = Master.query.get_or_404(master_id)
    data = request.get_json()
    bio = data.get('bio')

    if not bio:
        return jsonify({"error": "Bio is required"}), 400

    master.bio = bio
    db.session.commit()
    return jsonify({"message": "Bio updated successfully", "bio": master.bio}), 200

@masters_bp.route('/<int:master_id>/free-times', methods=['GET'])
def get_free_times(master_id):
    """Отримати список вільного часу для майстра"""
    master = Master.query.get_or_404(master_id)

    # Повертаємо вільний час або порожній список
    free_times = master.free_times if master.free_times else []

    return jsonify({"free_times": free_times}), 200



@masters_bp.route('/<int:master_id>/free-times', methods=['POST'])
def add_free_time(master_id):
    """Додати вільний час для майстра"""
    master = Master.query.get_or_404(master_id)
    data = request.get_json()
    free_time = data.get("free_time")

    if not free_time:
        return jsonify({"error": "Free time is required"}), 400

    # Додаємо вільний час у список
    if master.free_times is None:
        master.free_times = []
    master.free_times.append(free_time)

    db.session.commit()
    return jsonify({"message": "Free time added successfully", "free_times": master.free_times}), 201

@masters_bp.route('/<int:master_id>/appointments', methods=['GET'])
def get_master_appointments(master_id):
    """Отримати список клієнтів, які записалися до майстра"""
    bookings = Booking.query.filter_by(master_id=master_id).all()
    appointments = []

    for booking in bookings:
        user_data = User.query.get(booking.user_id)  # Отримуємо дані для кожного клієнта
        if user_data:  # Перевірка на існування користувача
            appointments.append({
                "id": booking.id,
                "client_name": f"{user_data.first_name} {user_data.last_name}",
                "booking_datetime": booking.booking_datetime.strftime("%Y-%m-%d %H:%M:%S")
            })

    return jsonify(appointments), 200

