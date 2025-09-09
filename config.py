import os

class Config:
    """
    Configurações do projeto FinanceApp.
    Variáveis podem ser definidas via ambiente ou usar defaults.
    """
    # -------------------------------
    # Flask
    # -------------------------------
    HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_PORT", 5000))
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() in ["true", "1", "yes", "s"]

    # -------------------------------
    # Google API
    # -------------------------------
    # Caminho do arquivo oauth_credentials.json
    CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS", "oauth_credentials.json")

    # -------------------------------
    # Outros parâmetros futuros
    # -------------------------------
    SHEET_NAMES = {
        "cards": "Cards",
        "control": "Control",
        "parcelados": "Parcelados"
    }
