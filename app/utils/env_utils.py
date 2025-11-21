import os

ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__ + "/..")), ".env")

def save_gemini_key(key: str):
    """Salva ou atualiza a chave GEMINI_API_KEY no .env"""
    key = key.strip()
    if not key:
        raise ValueError("Chave vazia")

    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.startswith("GEMINI_API_KEY="):
            lines[i] = f"GEMINI_API_KEY={key}\n"
            found = True
            break

    if not found:
        lines.append(f"GEMINI_API_KEY={key}\n")

    with open(ENV_FILE, "w") as f:
        f.writelines(lines)
