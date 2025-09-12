from flask import Blueprint
from .cards import cards_bp
from .control import control_bp
from .installments import recorrentes_bp

def register_routes(app):
    app.register_blueprint(cards_bp)
    app.register_blueprint(control_bp)
    app.register_blueprint(recorrentes_bp)

    @app.route("/")
    def home():
        return {"message": "API Finance App funcionando"}
