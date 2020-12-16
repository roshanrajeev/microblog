from flask import request
from flask_socketio import send
from app import socketio
from flask_login import current_user

live_users = {}

@socketio.on('connect')
def add_user():
    live_users[current_user.username] = request.sid

        