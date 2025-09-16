import os
import sys
import subprocess
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

class SetupDrive:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    def __init__(self, credentials_path="oauth_credentials.json", token_path="token.json", folder_name="FinanceApp", venv_dir="venv"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.folder_name = folder_name
        self.venv_dir = venv_dir

        self.setup_venv()              # Cria e ativa a venv
        self.creds = self.load_credentials()
        self.client = gspread.authorize(self.creds)
        self.drive_service = build("drive", "v3", credentials=self.creds)

    # -------------------
    # Credenciais Google
    # -------------------
    def load_credentials(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    os.remove(self.token_path)
                    return self.load_credentials()
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "w") as token_file:
                token_file.write(creds.to_json())
        return creds

    # -------------------
    # Pastas e Planilhas
    # -------------------
    def get_or_create_folder(self):
        query = f"name='{self.folder_name}' and mimeType='application/vnd.google-apps.folder'"
        results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        if files:
            print(f"📂 Pasta encontrada: {self.folder_name}")
            return files[0]["id"]
        else:
            folder_metadata = {"name": self.folder_name, "mimeType": "application/vnd.google-apps.folder"}
            folder = self.drive_service.files().create(body=folder_metadata, fields="id").execute()
            print(f"📂 Pasta criada: {self.folder_name}")
            return folder["id"]

    def get_or_create_spreadsheet(self, folder_id, sheet_name):
        try:
            spreadsheet = self.client.open(sheet_name)
            print(f"📄 Planilha encontrada: {sheet_name}")
        except gspread.SpreadsheetNotFound:
            spreadsheet = self.client.create(sheet_name)
            self.drive_service.files().update(fileId=spreadsheet.id, addParents=folder_id, fields="id, parents").execute()
            print(f"📄 Planilha criada: {sheet_name}")
            # Cabeçalhos iniciais
            sheet = spreadsheet.sheet1
            if sheet_name == "Cards":
                sheet.update("A1:D1", [["ID", "Nome", "Proprietario", "Ultimos_Digitos"]])
            elif sheet_name == "Control":
                sheet.update("A1:J1", [["ID","Nome","Tipo","Valor","Forma","Parcelas","Data","Cartao_ID","Modo","Status"]])
            elif sheet_name == "Recurrent":
                sheet.update("A1:J1", [["ID","Nome","Tipo","Valor","Forma","Parcelas","Data","Cartao_ID","Modo","Status"]])
            elif sheet_name == "Installment":
                sheet.update("A1:J1", [["ID","Nome","Tipo","Valor","Forma","Parcelas","Data","Cartao_ID","Modo","Status"]])
        return spreadsheet

    # -------------------
    # Virtualenv
    # -------------------
    def setup_venv(self, requirements_file="requirements.txt"):
        if not os.path.exists(self.venv_dir):
            print(f"🔧 Criando virtualenv em {self.venv_dir}...")
            subprocess.check_call([sys.executable, "-m", "venv", self.venv_dir])
        else:
            print(f"🔧 Virtualenv já existe em {self.venv_dir}")

        # Instalando requirements
        pip_path = os.path.join(self.venv_dir, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(self.venv_dir, "bin", "pip")
        if os.path.exists(requirements_file):
            print(f"📦 Instalando dependências de {requirements_file} na venv...")
            subprocess.check_call([pip_path, "install", "-r", requirements_file])
        else:
            print(f"⚠️ Arquivo {requirements_file} não encontrado.")

        # Ativando venv para o processo atual
        if not os.environ.get("VIRTUAL_ENV"):
            print("⚡ Ativando venv no processo atual...")
            bin_path = "Scripts" if os.name == "nt" else "bin"
            venv_bin = os.path.join(os.path.abspath(self.venv_dir), bin_path)
            os.environ["VIRTUAL_ENV"] = os.path.abspath(self.venv_dir)
            os.environ["PATH"] = venv_bin + os.pathsep + os.environ.get("PATH", "")
            print("✅ Venv ativada no processo atual.")
            print("🧪 Venv localizada em: "+os.environ.get("VIRTUAL_ENV"))

        else:
            print("✅ Já está dentro de uma venv, pulando ativação.")

    # -------------------
    # Setup completo
    # -------------------
    def setup(self):
        folder_id = self.get_or_create_folder()
        for sheet_name in ["Cards", "Control", "Recurrent", "Installment"]:
            self.get_or_create_spreadsheet(folder_id, sheet_name)
        print("✅ Setup completo!")
