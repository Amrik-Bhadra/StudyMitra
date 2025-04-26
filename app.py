from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Fetch API key from .env
API_KEY = os.getenv("OPENROUTER_API_KEY")

def chat_with_gpt(user_message, language_input):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a helpful student assistant that replies in {language_input}."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.get_json()
        user_message = data.get("message")
        language = data.get("language", "English")
        bot_reply = chat_with_gpt(user_message, language)
        return jsonify({"reply": bot_reply})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
