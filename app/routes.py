from flask import Blueprint, jsonify

bp = Blueprint("routes", __name__)

@bp.route("/")
def home():
    return jsonify({"message": "API Finance App funcionando"})
