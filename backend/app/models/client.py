from backend.app.extensions import db


class Client(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Використання id із User
    user = db.relationship('User', backref=db.backref('client', uselist=False))

    # Специфічні дані для клієнта (якщо потрібно)
    additional_info = db.Column(db.Text, nullable=True)  # Наприклад, якісь додаткові дані

    def to_dict(self):
        user_data = self.user.to_dict()  # Дані з таблиці User
        return {
            **user_data,  # Об'єднуємо дані з User
            "additional_info": self.additional_info
        }
