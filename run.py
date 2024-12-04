from backend.app import create_app
from backend.app.extensions import db
from backend.app.models.user import User
from datetime import datetime
import click

app = create_app()

@app.cli.command("create-admin")
@click.argument("email")
@click.argument("password")
def create_admin(email, password):
    """Команда для створення адміністратора"""
    # Перевірка, чи вже існує адміністратор з таким email
    if User.query.filter_by(email=email).first():
        print(f"Admin with email {email} already exists.")
        return

    # Створення адміністратора
    new_admin = User(
        role='admin',
        first_name="Admin",
        last_name="Admin",
        date_of_birth=datetime(2000, 1, 1),  # Дата народження за замовчуванням
        phone_number="0000000000",           # Телефон за замовчуванням
        email=email
    )
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()
    print(f"Admin with email {email} created successfully.")

if __name__ == "__main__":
    app.run()
