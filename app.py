from web_socket_server import WebSocketServer, socketio, app
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from flask_cors import CORS

app = WebSocketServer().create_app()
CORS(app)  
chat_rooms = {}


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']

    join_room(room)
    if room not in chat_rooms:
        chat_rooms[room] = []
    if username not in chat_rooms[room]:
        chat_rooms[room].append(username)

    emit("message", {"type": "notification", "message": f"{username} has joined the room."}, room=room)
    print(f"{username} joined room: {room}")

@socketio.on('message')
def on_message(data):
    room = data['room']
    message = data['message']
    username = data['username']

    send({"type": "message", "username": username, "message": message}, room=room)
    print(f"Message from {username} in room {room}: {message}")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('join_room.html')

if __name__ == '__main__':
    socketio.run(app)
