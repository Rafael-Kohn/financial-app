# importa os blueprints das rotas (seus arquivos de rota devem expor card_bp, control_bp, recurrent_bp, installment_bp)
from flask import Flask

def register_routes(app: Flask):
    try:
        from app.Routes.card import card_bp
        app.register_blueprint(card_bp)
    except Exception:
        # Se o arquivo foi nomeado diferente, ignore e continue
        pass

    try:
        from app.Routes.control import control_bp
        app.register_blueprint(control_bp)
    except Exception:
        pass

    try:
        from app.Routes.recurrent import recurrent_bp
        app.register_blueprint(recurrent_bp)
    except Exception:
        pass

    try:
        from app.Routes.installment import installment_bp
        app.register_blueprint(installment_bp)
    except Exception:
        pass

    # rota raiz simples
    @app.route("/")
    def home():
        return {"message": "API Finance App funcionando"}
