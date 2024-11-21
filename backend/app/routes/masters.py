from flask import Blueprint

masters_bp = Blueprint('masters', __name__)

@masters_bp.route('/')
def get_masters():
    return {"message": "Masters route works"}
