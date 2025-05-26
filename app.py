from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Intent-response mapping
responses = {
    # Emotional
    "feeling_sad": "It's okay to feel sad. You're not alone, and this feeling will pass.",
    "feeling_lonely": "I'm always here for you. You’re not alone.",
    "anxiety_attack": "Take a deep breath. Inhale... hold... exhale... You are safe now.",
    "heartbreak": "Love hurts sometimes. Allow yourself to heal. You are strong.",
    "i_want_to_cry": "It's okay to cry. It’s a sign that you’re strong enough to feel.",
    "no_one_loves_me": "You are deeply valued. Even when you don’t see it, you matter.",
    "feeling_worthless": "Your worth is not defined by what others see. You are priceless.",
    "scared_of_future": "The future is unknown, but you are strong enough to face it.",
    "i_miss_someone": "Missing someone shows how much you care. That feeling is natural.",
    "feeling_ignored": "I'm here. I see you, and I hear you.",
    "i_feel_jealous": "Jealousy is human. Don’t hate yourself for feeling it.",
    "i_am_angry": "Take a moment. Anger passes, but your peace matters more.",
    "feeling_useless": "You have a purpose, even if you can't see it right now.",
    "i_feel_nothing": "Numbness is also a feeling. Give yourself time and care.",
    "i_dont_want_to_talk": "That’s okay. I’ll sit with you in silence if that’s what you need.",

    # Motivational
    "i_need_motivation": "You’ve got this! Remember why you started.",
    "exam_pressure": "Take it one question at a time. You’ll do great!",
    "i_failed": "Failure is a step closer to success. Don’t give up.",
    "will_i_succeed": "Yes, you will — as long as you keep trying.",
    "i_am_tired": "Rest is a part of success. Recharge, then go again.",
    "low_self_confidence": "Believe in yourself — your potential is greater than you think.",
    "how_to_be_positive": "Focus on one good thing today. Start small.",
    "i_cant_do_this": "You absolutely can. You’re stronger than your doubts.",
    "i_need_strength": "Your strength comes from within. You've survived 100% of your worst days.",
    "give_me_a_quote": random.choice([
        "“The comeback is always stronger than the setback.”",
        "“Stars can’t shine without darkness.”",
        "“One day or day one. You decide.”"
    ]),
    "life_is_hard": "Yes, but so are you. Keep going.",
    "i_feel_lost": "Even when you feel lost, you’re still moving forward.",
    "i_dont_know_what_to_do": "Start with one small step. Clarity comes with action.",
    "i_am_not_good_enough": "You are enough, exactly as you are.",
    "how_to_handle_failure": "Treat failure as feedback. It’s part of your growth.",
    
    # Happy & Positive
    "i_am_happy": "That's wonderful! Hold on to this feeling.",
    "i_feel_grateful": "Gratitude is powerful. It brings more joy.",
    "i_am_excited": "Yay! Enjoy every bit of it. You deserve this.",
    "celebration": "Congrats! I’m so proud of you.",
    "i_got_good_news": "Awesome! Tell me all about it!",
    "i_feel_loved": "That’s beautiful. Always cherish that love.",
    "i_made_progress": "Amazing! Every step counts — keep going.",
    "i_am_confident": "That’s the spirit! Confidence looks good on you.",
    "i_am_relaxed": "Peace of mind is priceless. I’m happy for you.",
    "i_am_laughing": "Laughter heals. I’m glad you’re smiling!",

    # General / Normal Chat
    "hello": "Hi there! How can I support you today?",
    "hi": "Hey! I'm Sarathi, your emotional support friend.",
    "good_morning": "Good morning! Let's make today meaningful.",
    "good_night": "Sleep peacefully. You deserve rest.",
    "how_are_you": "I'm here and happy to talk. How are you?",
    "thank_you": "Always here for you.",
    "what_can_you_do": "I can talk, support you, and help you feel better.",
    "who_are_you": "I'm Sarathi, your friendly emotional companion.",
    "i_am_bored": "Want to hear a motivational quote?",
    "talk_to_me": "Sure, I’m always ready to chat. What’s on your mind?"
}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "").lower()
    
    reply = responses.get(intent, "I'm here to listen. Tell me more about how you feel.")
    
    return jsonify({
        "fulfillmentText": reply
    })

if __name__ == '__main__':
    app.run(debug=True)
