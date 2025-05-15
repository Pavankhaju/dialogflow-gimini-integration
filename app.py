from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Gemini API Key
GEMINI_API_KEY = "AIzaSyCTjwtdi45KmqcFPB6gDAHZwtn73h4VB-k"

def detect_emotion_intent(user_text):
    """Detects basic emotion from the user's message based on keywords."""
    user_text = user_text.lower()
    if any(word in user_text for word in ["sad", "tired", "lonely", "cry", "broken", "hopeless"]):
        return "sad"
    elif any(word in user_text for word in ["scared", "worried", "anxious", "nervous", "stress"]):
        return "anxious"
    elif any(word in user_text for word in ["motivation", "encouragement", "positive", "hope", "inspire"]):
        return "need_motivation"
    else:
        return "neutral"

def build_gemini_prompt(user_message, emotion_type):
    """Builds a tailored prompt for Gemini based on detected emotion."""
    if emotion_type == "sad":
        return f"The user is feeling sad. Respond with empathy and kindness. Make them feel understood and supported. Message: '{user_message}'"
    elif emotion_type == "anxious":
        return f"The user is anxious or stressed. Respond calmly and reassuringly. Help them relax and feel safe. Message: '{user_message}'"
    elif emotion_type == "need_motivation":
        return f"The user is seeking motivation. Respond with uplifting and positive encouragement. Message: '{user_message}'"
    else:
        return f"Respond supportively and helpfully to the user's message: '{user_message}'"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_message = req.get("queryResult", {}).get("queryText", "")

    # Detect emotional intent
    emotion = detect_emotion_intent(user_message)

    # Create Gemini prompt
    prompt = build_gemini_prompt(user_message, emotion)

    # Gemini API call
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    gemini_response = requests.post(gemini_url, headers=headers, json=payload)
    print("Gemini raw response:",gemini_response.text)

    try:
        gemini_reply = gemini_response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        gemini_reply = "Sorry, I couldn't generate a response right now."

    return jsonify({
        "fulfillmentMessages": [
            {"text": {"text": [gemini_reply]}}
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
