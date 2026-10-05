from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")

def send_whatsapp(phone, message):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"
    payload = {"phone": phone, "message": message}
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Finbot online!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        phone = data.get("phone")
        text_obj = data.get("text", {})
        msg = text_obj.get("message") or text_obj.get("body") or ""
        
        if not phone or not msg:
            return jsonify({"ok": True})

        if "gastei" in msg.lower() or "paguei" in msg.lower():
            resposta = f"Anotado! 💰 {msg}\nVou salvar na sua planilha em breve."
        else:
            resposta = f"Fala! Sou seu Finbot. Manda um gasto tipo: gastei 20 no uber"

        send_whatsapp(phone, resposta)
    except Exception as e:
        print(e)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
