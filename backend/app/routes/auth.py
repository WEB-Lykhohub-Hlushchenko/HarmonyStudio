from flask import Blueprint, request, jsonify
from backend.app.models.user import User
from backend.app.models.client import Client
from backend.app.models.master import Master
from backend.app.extensions import db
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Реєстрація нового користувача (клієнт або майстер).
    """
    try:
        data = request.get_json()
        role = data.get('role')

        if role not in ['client', 'master']:
            return jsonify({"error": "Invalid role. Must be 'client' or 'master'"}), 400

        # Перевірка існуючого email
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({"error": "Email already exists"}), 400

        # Створення користувача
        new_user = User(
            role=role,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=datetime.strptime(data.get('date_of_birth'), "%Y-%m-%d"),
            phone_number=data.get('phone_number'),
            email=data.get('email')
        )
        new_user.set_password(data.get('password'))

        db.session.add(new_user)
        db.session.commit()

        # Прив'язка до відповідної моделі залежно від ролі
        if role == 'client':
            new_client = Client(id=new_user.id)
            db.session.add(new_client)
        elif role == 'master':
            new_master = Master(id=new_user.id)
            db.session.add(new_master)

        db.session.commit()
        return jsonify({"message": f"{role.capitalize()} registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Вхід у систему для всіх типів користувачів.
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Перевірка ролі користувача та перенаправлення
            if user.role == 'admin':
                return jsonify({
                    "message": "Welcome to the admin panel",
                    "redirect": "/admin",
                    "user": user.to_dict()
                }), 200
            elif user.role == 'client':
                return jsonify({
                    "message": "Welcome to the client dashboard",
                    "redirect": "/client-dashboard",
                    "user": user.to_dict()
                }), 200
            elif user.role == 'master':
                return jsonify({
                    "message": "Welcome to the master dashboard",
                    "redirect": "/master-dashboard",
                    "user": user.to_dict()
                }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


