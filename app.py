from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, send, emit
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

chat_rooms = {}

@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]

    join_room(room)
    if room not in chat_rooms:
        chat_rooms[room] = []
    if username not in chat_rooms[room]:
        chat_rooms[room].append(username)

    emit("message", {
        "type": "notification",
        "message": f"{username} has joined the room."
    }, room=room)
    print(f"{username} joined room: {room}")

@socketio.on("message")
def on_message(data):
    room = data["room"]
    message = data["message"]
    username = data["username"]

    send({
        "type": "message",
        "username": username,
        "message": message
    }, room=room)
    print(f"Message from {username} in room {room}: {message}")

@app.route('/')
def index():
    return render_template('join_room.html')

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)

