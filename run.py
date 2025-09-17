import os
#-------------------------------
# Valida ou solicita as variáveis
# -------------------------------

host = os.environ.get("FLASK_HOST") or input("Digite o IP ou enter para default [0.0.0.0]: ").strip() or "0.0.0.0"
port = int(os.environ.get("FLASK_PORT") or input("Digite a porta ou enter para default [:5000]: ").strip() or 5000)
debug_env = os.environ.get("FLASK_DEBUG")
debug = str(debug_env).lower() in ["true", "1", "s", "sim"] if debug_env else True

credentials_path = os.environ.get("GOOGLE_CREDENTIALS") or input("Digite o path das credenciais OAuth ou enter para default [oauth_credentials.json]: ").strip() or "oauth_credentials.json"

# Atualiza variáveis de ambiente
os.environ["FLASK_HOST"] = host
os.environ["FLASK_PORT"] = str(port)
os.environ["FLASK_DEBUG"] = str(debug)
os.environ["GOOGLE_CREDENTIALS"] = credentials_path

# -------------------------------
# Setup Venv
# -------------------------------
from setup_venv import EnvManager

setup_venv= EnvManager()
setup_venv.setup()

# -------------------------------
# Setup Google Drive/Sheets
# -------------------------------
from app.Utils.setup_drive import SetupDrive

setup_drive= SetupDrive(credentials_path)
setup_drive.setup()
# -------------------------------
# Inicializa Flask
# -------------------------------
from app import create_app

print(f"\n🚀 Inicializando FinanceApp no {host}:{port} (Debug: {debug})\n")
app = create_app()
app.config["setup_drive"] = setup_drive
app.run(host=host, port=port, debug=debug, use_reloader=False)
