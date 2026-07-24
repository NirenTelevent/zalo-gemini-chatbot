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


def home():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


