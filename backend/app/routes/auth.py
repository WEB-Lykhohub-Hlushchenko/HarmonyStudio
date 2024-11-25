from flask import Blueprint, request, jsonify
from backend.app.models.user import User
from backend.app.models.client import Client
from backend.app.extensions import db
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        role = data.get('role')
        if role != 'client':
            return jsonify({"error": "Only clients can register here"}), 400

        # Перевірка існуючого email
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({"error": "Email already exists"}), 400

        # Створюємо користувача
        new_user = User(
            role='client',
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=datetime.strptime(data.get('date_of_birth'), "%Y-%m-%d"),
            phone_number=data.get('phone_number'),
            email=data.get('email')
        )
        new_user.set_password(data.get('password'))

        db.session.add(new_user)
        db.session.commit()

        # Створюємо клієнта
        new_client = Client(id=new_user.id)
        db.session.add(new_client)
        db.session.commit()

        return jsonify({"message": "Client registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500



@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if user.role == 'admin':
                # Якщо користувач — адміністратор
                return jsonify({
                    "message": "Welcome to the admin panel",
                    "redirect": "/admin",
                    "user": user.to_dict()
                }), 200
            else:
                # Якщо користувач — клієнт або майстер
                return jsonify({
                    "message": "Login successful",
                    "redirect": "/home",
                    "user": user.to_dict()
                }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


# Маршрут для створення адміністратора
@auth_bp.route('/create-admin', methods=['POST'])
def create_admin():
    try:
        data = request.get_json()

        # Перевірка існуючого email
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({"error": "Admin with this email already exists"}), 400

        new_admin = User(
            role='admin',
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=datetime.strptime(data.get('date_of_birth'), "%Y-%m-%d"),
            phone_number=data.get('phone_number'),
            email=data.get('email')
        )
        new_admin.set_password(data.get('password'))
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({"message": "Admin created successfully"}), 201
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
