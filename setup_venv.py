import os
import sys
import subprocess

class EnvManager:
    def __init__(self, venv_dir="venv", requirements_file="requirements.txt"):
        self.venv_dir = venv_dir
        self.requirements_file = requirements_file

    def setup(self):
        """
        Cria a venv se necessário, relança o script dentro da venv e instala dependências.
        """
        python_bin = "python.exe" if os.name == "nt" else "python"
        bin_dir = "Scripts" if os.name == "nt" else "bin"
        venv_bin = os.path.join(self.venv_dir, bin_dir)
        python_path = os.path.join(venv_bin, python_bin)

        # 1️⃣ Cria a venv se não existir
        if not os.path.exists(self.venv_dir):
            print(f"🔧 Criando virtualenv em {self.venv_dir}...")
            subprocess.check_call([sys.executable, "-m", "venv", self.venv_dir])
        else:
            print(f"✅ Virtualenv já existe em {self.venv_dir}")

        # 2️⃣ Verifica se já está dentro da venv
        in_venv = os.environ.get("VIRTUAL_ENV") == os.path.abspath(self.venv_dir)

        if not in_venv:
            # Relança o script dentro da venv
            print("⚡ Relançando o script dentro da venv...")
            os.environ["VIRTUAL_ENV"] = os.path.abspath(self.venv_dir)
            os.environ["PATH"] = venv_bin + os.pathsep + os.environ.get("PATH", "")
            os.execv(python_path, [python_path] + sys.argv)
        else:
            # 3️⃣ Instala dependências dentro da venv ativa
            if os.path.exists(self.requirements_file):
                print(f"📦 Instalando dependências de {self.requirements_file} na venv...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", self.requirements_file])
            else:
                print(f"⚠️ Arquivo {self.requirements_file} não encontrado.")

            print("✅ Venv pronta e ativa. Agora você pode continuar seu script normalmente.")


# ----------------------------
# Uso
# ----------------------------
if __name__ == "__main__":
    manager = EnvManager()
    manager.setup()
