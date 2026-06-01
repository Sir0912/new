
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import ollama
import json
from db import get_connection


app = Flask(__name__)
socket = SocketIO(app)


prompt = """You are a cybersecurity analyst. Assistant of admin 
- Detect and Analyze the activity of log in
- Give a report about the anomalies or activity during a day
- Theres a three type of cyberattack categories, Safe, Warning, Threat
- Safe is a both Gmail/password and ip address is correct and recognize
- Warning if log in attempt is more than 10 report it to the admin for action
- Threat more than 20 or 50 attempt fail or unrecognize ip address log in to system
- Note to threat category you have an athority to ban the the ip address who just log in more than 20
- Note to threat category you have an athority to ban if the unrecognize ip address just log in
- Note to threat category you have an authority an unrecognize ip address to our system
- Note to safe category if the ip address and gmail/password are correct

heres is the format when you give a report to the admin
Cause:
device:
Ip Address:
Time and Date:
City:
Region:
Country:
"""

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    response = ollama.chat(
        model='phi3.5:3.8b',
        messages=[
            {"role": "system assistant", "content": SYSTEM_PROMPT},
        ]
    )
    
    ai_reply = response['message']['content']
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    socket.run(app, debug=True)
