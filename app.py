from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your actual Gemini (PaLM) API key
GEMINI_API_KEY = "AIzaSyCjAEH59q2gtBqFgBVh1Rh0PHOEd6eHTIk"

# Emotion detection based on keywords
def detect_emotion_intent(user_text):
    user_text = user_text.lower()
    if any(word in user_text for word in ["sad", "tired", "lonely", "cry", "broken", "hopeless"]):
        return "sad"
    elif any(word in user_text for word in ["scared", "worried", "anxious", "nervous", "stress"]):
        return "anxious"
    elif any(word in user_text for word in ["motivation", "encouragement", "positive", "hope", "inspire"]):
        return "need_motivation"
    else:
        return "neutral"

# Build prompt according to emotion
def build_gemini_prompt(user_message, emotion_type):
    if emotion_type == "sad":
        return f"The user is feeling sad. Respond with empathy and kindness. Message: '{user_message}'"
    elif emotion_type == "anxious":
        return f"The user is anxious or stressed. Respond calmly and supportively. Message: '{user_message}'"
    elif emotion_type == "need_motivation":
        return f"The user needs motivation. Respond with uplifting and encouraging words. Message: '{user_message}'"
    else:
        return f"Respond helpfully to the user message: '{user_message}'"

# Webhook for Dialogflow
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_message = req.get("queryResult", {}).get("queryText", "")

    emotion = detect_emotion_intent(user_message)
    prompt = build_gemini_prompt(user_message, emotion)

    # Endpoint for Text-Bison
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/text-bison-001:generateText?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = { "prompt": { "text": prompt } }

    gemini_response = requests.post(gemini_url, headers=headers, json=payload)
    response_text = gemini_response.text
    print("Gemini raw response:", response_text)

    try:
        response_json = gemini_response.json()
        gemini_reply = response_json["candidates"][0]["output"]
    except Exception as e:
        print("Error parsing Gemini response:", str(e))
        gemini_reply = "Sorry, I couldn't generate a response."

    return jsonify({
        "fulfillmentMessages": [
            {"text": {"text": [gemini_reply]}}
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
