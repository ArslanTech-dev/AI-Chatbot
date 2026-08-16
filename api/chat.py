import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fallback if no API key is set
def fallback_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hello! I'm ARSLAN TECH'S AI Chatbot. How can I help you?"
    elif "your name" in user_input:
        return "I am ARSLAN TECH'S AI Chatbot, created with Python and Flask."
    elif "bye" in user_input:
        return "Goodbye! Have a great day."
    else:
        return "I'm a simple fallback bot. Set OPENAI_API_KEY in .env to enable full AI responses."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please send a message."}), 400

    if os.getenv("OPENAI_API_KEY"):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant created by ARSLAN TECH."},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=150
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error calling OpenAI API: {str(e)}"
    else:
        reply = fallback_response(user_message)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)