from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    new_user = User(first_name="Test", last_name="User", email="test@example.com", password="12345", role="user")
    db.session.add(new_user)
    db.session.commit()

    print("Користувач успішно доданий!")
