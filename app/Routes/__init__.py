from flask import Flask, jsonify

def register_routes(app: Flask):
    """
    Registra todos os blueprints manualmente de forma clara.
    """

    # Lista de módulos de rota e seus blueprints
    routes = [
        ("app.Routes.card", "card_bp"),
        ("app.Routes.control", "control_bp"),
        ("app.Routes.installment", "installment_bp"),
        ("app.Routes.recurrent", "recurrent_bp")
    ]

    for module_path, bp_name in routes:
        try:
            module = __import__(module_path, fromlist=[bp_name])
            blueprint = getattr(module, bp_name)
            app.register_blueprint(blueprint)
            print(f"✅ Blueprint registrado: {bp_name}")
        except (ImportError, AttributeError) as e:
            print(f"⚠️ {bp_name} não encontrado em {module_path}, ignorando... ({e})")

    # Rota raiz
    @app.route("/")
    def home():
        return jsonify({"message": "API Finance App funcionando 🚀"})
