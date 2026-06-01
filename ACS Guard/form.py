from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_socketio import SocketIO # 1. Import the radio broadcaster tool
from db import get_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def landing_page():
    return render_template("cyber_log.html")

@app.route("/home", methods=["POST"])
def home_page():
    admin = request.form.get("admin")
    password = request.form.get("passcode")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE name=%s AND password=%s", (admin, password))
    account_found = cursor.fetchone()
    conn.close()
    
    if account_found:
        session["logged_in"] = True
        session["user"] = admin
        return redirect(url_for("scan_page"))
    return redirect(url_for("landing_page"))

@app.route("/scan")
def scan_page():
    if not session.get("logged_in"):
        return redirect(url_for("landing_page"))
    return render_template("scan.html")

# This is where your physical hardware/RFID reader sends the scanned ID card
@app.route("/api/scan", methods=["POST"])
def api_scan():
    uid = request.form.get("uid") or request.get_json(force=True).get("uid")
    if not uid:
        return jsonify({"status": "error"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE rfid = %s", (uid,))
    admin = cursor.fetchone()
    
    if admin:
        cursor.execute("UPDATE admin SET last_scan = NOW() WHERE rfid = %s", (uid,))
        conn.commit()
        socketio.emit('card_scanned', {"name": admin["name"], "authorized": True})
    else:
        socketio.emit('card_scanned', {"name": "Unknown", "authorized": False})
        
    conn.close()
    return jsonify({"status": "success"})

@app.route("/cyber_dash")
def cyber_dash():
    return render_template("cyber_dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing_page"))

if __name__ == "__main__":
    socketio.run(app, debug=True)