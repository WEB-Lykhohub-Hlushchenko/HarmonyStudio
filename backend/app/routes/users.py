from flask import Blueprint, jsonify
from backend.app.models.user import User
from backend.app.models.master import Master
from backend.app.models.client import Client
from backend.app.extensions import db
from backend.app.models.booking import Booking

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Отримати інформацію про користувача та його специфічні дані"""
    user = User.query.get_or_404(user_id)

    # Базова інформація про користувача
    response = user.to_dict()

    # Додаємо дані для майстра
    if user.role == "master":
        master = Master.query.filter_by(user_id=user.id).first()
        if master:
            response.update({
                "bio": master.bio or "No bio available",
                "service_id": master.service_id
            })

    # Додаємо дані для клієнта
    elif user.role == "client":
        client = Client.query.filter_by(id=user.id).first()
        if client and hasattr(client, 'appointments'):
            response.update({
                "appointments": [
                    {
                        "id": booking.id,
                        "master_id": booking.master_id,
                        "service_id": booking.service_id,
                        "booking_datetime": booking.booking_datetime
                    }
                    for booking in client.appointments
                ]
            })

    return jsonify(response), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Видалити користувача та всі пов'язані дані"""
    user = User.query.get_or_404(user_id)

    # Видаляємо записи користувача
    Booking.query.filter_by(user_id=user.id).delete()

    # Видаляємо специфічні дані залежно від ролі
    if user.role == "client":
        Client.query.filter_by(id=user.id).delete()
    elif user.role == "master":
        Master.query.filter_by(user_id=user.id).delete()

    # Видаляємо самого користувача
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

