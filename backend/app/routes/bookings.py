from flask import Blueprint

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
def get_bookings():
    return {"message": "Bookings route works"}
