import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in environment")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages")
    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    resp = openai.chat.completions.create(
        model="gpt-4o-mini",      # or "gpt-4" / "gpt-3.5-turbo"
        messages=messages
    )
    bot_msg = resp.choices[0].message.content
    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    # Serve on HTTP default port 80
    app.run(host="0.0.0.0", port=80, debug=True)


