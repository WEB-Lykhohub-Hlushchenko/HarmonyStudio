from flask import Blueprint

faq_bp = Blueprint('faq', __name__)

@faq_bp.route('/')
def get_faq():
    return {"message": "FAQ route works"}
