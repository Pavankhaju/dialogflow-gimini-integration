from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Gemini API Key yahan daalo
GEMINI_API_KEY = "AIzaSyCTjwtdi45KmqcFPB6gDAHZwtn73h4VB-k"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_message = req.get("queryResult", {}).get("queryText", "")

    # Gemini API call
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }

    gemini_response = requests.post(gemini_url, headers=headers, json=payload)

    try:
        gemini_reply = gemini_response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        gemini_reply = "Sorry, I couldn't generate a response."

    return jsonify({
        "fulfillmentMessages": [
            {"text": {"text": [gemini_reply]}}
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
