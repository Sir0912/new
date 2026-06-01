from flask import Flask, render_template, jsonify, request
from flask import session, redirect, url_for
import json
from flask_socketio import SocketIO
import mysql.connector
from db import get_connection

app = Flask(__name__)
socket = SocketIO(app)

if __name__ == "__main__":
    socket.run(app, debug=True)