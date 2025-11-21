import requests
from config import GEMINI_API_KEY, MODEL

chat_history = []

def ask_gemini(prompt):
    global chat_history

    chat_history.append({"role": "user", "parts": [{"text": prompt}]})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"

    payload = {"contents": chat_history}

    r = requests.post(url, json=payload)

    try:
        resposta = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        chat_history.append({"role": "model", "parts": [{"text": resposta}]})
        return resposta
    except:
        return f"Erro: {r.text}"
