# app.py
import os
import shutil

from dotenv import load_dotenv

load_dotenv()

import requests
from flask import Flask, jsonify, render_template, request, session

from agent_docsearch import agent_tracuu_tailieu
from chatbot_prompts import SYSTEM_PROMPT
from flask_session import Session

if os.path.exists("flask_session"):
    shutil.rmtree("flask_session")

# === Cấu hình Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# API KEY
API_KEY = api_key=os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def call_gemini_api(user_input, history=[]):
    headers = {"Content-Type": "application/json"}

    contents = []

    # Chỉ thêm SYSTEM_PROMPT nếu history đang rỗng (tức lần đầu)
    if not history:
        contents.append({"role": "model", "parts": [{"text": SYSTEM_PROMPT}]})

    #  Chỉ thêm doc_info nếu lần đầu hoặc nếu bạn muốn dán lại khi liên quan
    doc_info = agent_tracuu_tailieu(user_input)
    if doc_info :
        contents.append({"role": "model", "parts": [{"text": doc_info}]})

    # Thêm phần lịch sử hội thoại
    for role, message in history:
        contents.append({
            "role": "user" if role == "user" else "model",
            "parts": [{"text": message}]
        })

    # Thêm câu hỏi mới
    contents.append({"role": "user", "parts": [{"text": user_input}]})
    data = {"contents": contents}

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Lỗi kết nối: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_question = data.get("question", "")

    # Tạo history nếu chưa có
    if "chat_history" not in session:
        session["chat_history"] = []

    chat_history = session["chat_history"]

    # Định dạng lại history để gửi cho Gemini
    formatted_history = []
    for msg in chat_history:
        formatted_history.append((msg["role"], msg["message"]))

    # Gọi API Gemini
    answer = call_gemini_api(user_question, formatted_history)

    # Cập nhật lại lịch sử chat
    chat_history.append({"role": "user", "message": user_question})
    chat_history.append({"role": "bot", "message": answer})
    session["chat_history"] = chat_history

    return jsonify({"answer": answer})



if __name__ == "__main__":
    app.run(debug=True)
