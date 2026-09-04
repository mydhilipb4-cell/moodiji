from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)
MAX_TEXT_LENGTH = 500

EMOJIS = {
    "happy": "😎", "sad": "🥲", "love": "❤️", "angry": "😤",
    "tired": "🥱", "sleep": "😴", "exam": "📝", "school": "🏫",
    "study": "📚", "studying": "📖", "work": "💻", "money": "💸",
    "food": "🍔", "eat": "🍽️", "coffee": "☕", "home": "🏠",
    "friend": "🫂", "friends": "🫂", "party": "🎉", "music": "🎵",
    "game": "🎮", "gaming": "🎮", "phone": "📱", "computer": "💻",
    "rain": "🌧️", "sun": "☀️", "hot": "🥵", "cold": "🥶",
    "fire": "🔥", "fast": "💨", "run": "🏃", "running": "🏃",
    "walk": "🚶", "car": "🚗", "travel": "✈️", "trip": "🧳",
    "today": "📅", "tomorrow": "⏰", "night": "🌙", "morning": "🌅",
    "yes": "✅", "no": "❌", "not": "🚫", "why": "❓", "what": "🤨",
    "wow": "🤯", "sorry": "🙏", "please": "🥺", "lol": "😂",
    "laugh": "😂", "cry": "😭", "dead": "💀", "help": "🆘",
    "boss": "👔", "teacher": "🧑‍🏫", "test": "📝", "exam": "📝",
    "win": "🏆", "won": "🏆", "fail": "📉", "failed": "📉",
    "buy": "🛒", "shopping": "🛍️", "money": "💰"
}

OPPOSITE_EMOJIS = {
    "happy": "🥲", "sad": "😎", "love": "😤", "angry": "❤️",
    "tired": "⚡", "sleep": "☀️", "hot": "🥶", "cold": "🥵",
    "yes": "❌", "no": "✅", "win": "📉", "won": "📉",
    "fail": "🏆", "failed": "🏆", "fast": "🐢", "run": "🛋️",
    "running": "🛋️", "laugh": "😭", "cry": "😂", "friend": "🚶",
    "friends": "🚶", "morning": "🌙", "night": "🌅"
}

FILLER = {"i", "a", "an", "the", "to", "of", "and", "or", "is", "am",
          "are", "was", "were", "have", "has", "had", "my", "me", "you",
          "your", "we", "they", "it", "in", "on", "for", "with", "this",
          "that", "just", "be", "been", "do", "did", "will", "can"}

def translate(text):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    out = []
    for word in words:
        if word in EMOJIS:
            out.append(EMOJIS[word])
        elif word not in FILLER:
            # Turn unknown words into a tiny "AI chaos" symbol.
            out.append(random.choice(["✨", "🔤", "🫠", "🗿", "👀", "💭"]))
    if not out:
        return "🫥"
    # Add expressive punctuation based on sentence mood.
    lower = text.lower()
    if "?" in text:
        out.insert(0, "🤔")
        out.append("❓")
    if "!" in text:
        out.append("‼️")
    if any(x in lower for x in ["lol", "haha", "funny"]):
        out.append("😂")
    if any(x in lower for x in ["very", "really", "so "]):
        out.insert(0, "🔥")
    return " ".join(out)

def useless_score(original, result):
    # Deliberately meaningless score: more words + more emoji chaos = more useless.
    words = len(re.findall(r"\w+", original))
    emojis = len(result.split())
    score = min(100, 35 + words * 4 + emojis * 5 + random.randint(0, 25))
    return score

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/translate")
def api_translate():
    data = request.get_json(silent=True) or {}
    text, error = get_text(data, "Type something first 😭")
    if error:
        return jsonify({"error": error}), 400
    result = translate(text)
    return jsonify({
        "translation": result,
        "score": useless_score(text, result)
    })

@app.post("/regenerate")
def regenerate():
    data = request.get_json(silent=True) or {}
    text, error = get_text(data, "Nothing to regenerate yet.")
    if error:
        return jsonify({"error": error}), 400
    result = translate(text)
    return jsonify({"translation": result, "score": useless_score(text, result)})


def get_text(data, empty_message):
    if not isinstance(data, dict):
        return "", "Request body must be a JSON object."

    text = data.get("text")
    if not isinstance(text, str):
        return "", "Text must be a string."

    text = text.strip()
    if not text:
        return "", empty_message
    if len(text) > MAX_TEXT_LENGTH:
        return "", f"Text must be {MAX_TEXT_LENGTH} characters or fewer."
    return text, None

if __name__ == "__main__":
    app.run()
