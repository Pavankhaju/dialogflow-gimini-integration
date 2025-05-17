from flask import Flask, request, jsonify
import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(_name_)

# Service Account JSON file path yahan de
SERVICE_ACCOUNT_PATH = "C:/Users/ratho/OneDrive/Desktop/json/sarthibot-surl-88ef1c1c0fd1"
port = int(os.getenv("PORT",5000))


# Scopes required for PaLM API
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# Authenticate using service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Authorized session banate hain jo API requests karega
authed_session = AuthorizedSession(credentials)

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

def build_gemini_prompt(user_message, emotion_type):
    if emotion_type == "sad":
        return f"The user is feeling sad. Respond with empathy and kindness. Message: '{user_message}'"
    elif emotion_type == "anxious":
        return f"The user is anxious or stressed. Respond calmly and supportively. Message: '{user_message}'"
    elif emotion_type == "need_motivation":
        return f"The user needs motivation. Respond with uplifting and encouraging words. Message: '{user_message}'"
    else:
        return f"Respond helpfully to the user message: '{user_message}'"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_message = req.get("queryResult", {}).get("queryText", "")

    emotion = detect_emotion_intent(user_message)
    prompt = build_gemini_prompt(user_message, emotion)
    print("Prompt sent to Gemini:", prompt)

    # PaLM Text-Bison API endpoint
    gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/text-bison-001:generateText"

    payload = {
        "prompt": {
            "text": prompt
        }
    }

    # Authorized request using service account credentials
    gemini_response = authed_session.post(gemini_url, json=payload)
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

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
