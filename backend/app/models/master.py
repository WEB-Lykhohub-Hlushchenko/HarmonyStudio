from backend.app.extensions import db

class Master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    free_times = db.Column(db.JSON, nullable=True)  # Поле для вільного часу

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "bio": self.bio,
            "free_times": self.free_times or []  # Повертаємо пустий список, якщо немає вільного часу
        }
