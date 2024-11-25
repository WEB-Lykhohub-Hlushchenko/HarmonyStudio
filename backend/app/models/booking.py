from backend.app.extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    booking_datetime = db.Column(db.DateTime, nullable=False)  # Дата та час бронювання
    status = db.Column(db.String(50), nullable=False)  # Наприклад, "pending", "confirmed", "cancelled"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "master_id": self.master_id,
            "service_id": self.service_id,
            "booking_datetime": self.booking_datetime.isoformat() if self.booking_datetime else None,
            "status": self.status
        }
