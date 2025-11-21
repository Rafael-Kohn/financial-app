from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
DB_NAME = "financial.db"
EXPORT_FILE = "export_gastos.xlsx"
