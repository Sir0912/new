from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from db import verify_login

app = Flask(__name__)
app.secret_key = "blackpower"

@app.route("/")
def login_page():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    ip = request.remote_addr
    
    employee = verify_login(email, password)
    
    if employee:
        session["logged_in"] = True
        session["email"] = employee["gmail"]
        session["name"] = employee["name"]
        session["ip"] = ip
        
        return jsonify({"status": "success", "name": session["name"]})
    
    return jsonify({"status": "error", "message": "Invalid email or password"})

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))
    
    return render_template("dashboard.html", 
                        name=session["name"],
                        email=session["email"],
                        ip=session["ip"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)