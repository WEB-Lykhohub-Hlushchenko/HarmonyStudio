from backend.app import create_app
from backend.app.extensions import db
from backend.app.models.user import User
from datetime import datetime
import click
from flask_cors import CORS

app = create_app()
CORS(app)


# Команда для створення адміністратора
@app.cli.command("create-admin")
@click.argument("email")
@click.argument("password")
def create_admin(email, password):
    if User.query.filter_by(email=email).first():
        print(f"Admin with email {email} already exists.")
        return

    new_admin = User(
        role='admin',
        first_name="Admin",
        last_name="Admin",
        date_of_birth=datetime(2000, 1, 1),  # Дата народження за замовчуванням
        phone_number="0000000000",  # Телефон за замовчуванням
        email=email
    )
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()
    print(f"Admin with email {email} created successfully.")


# Команда для оновлення пароля адміністратора
@app.cli.command("update-admin-password")
@click.argument("email")
@click.argument("new_password")
def update_admin_password(email, new_password):
    admin = User.query.filter_by(email=email).first()
    if not admin:
        print(f"No admin found with email {email}.")
        return

    admin.set_password(new_password)
    db.session.commit()
    print(f"Password for admin {email} updated successfully.")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
