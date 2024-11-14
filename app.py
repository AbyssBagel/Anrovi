from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# This dictionary will store the users that are connected to the server
users = {}

@app.route('/')
def index():
  return render_template('index.html')

# This function will be called when the client connects to the server
@socketio.on("connect")
def handle_connect():
  username = f"User_{random.randint(1000, 9999)}" # This is a random username
  private_key = random.randint(100000, 999999) # This is a private key that will be used to encrypt the message

  users[request.sid] = {"username": username, "private_key": private_key}

  emit("connected", {"username": username}, broadcast=True)
  emit("set_username", {"username": username})

# This function will be called when the client disconnects from the server
@socketio.on("disconnect")
def handle_disconnect():
  user = users.pop(request.sid, None)
  if user:
    emit("disconnected", {"username": user["username"]}, broadcast=True)

# This function will be called when the client sends a message
@socketio.on("send_message")
def handle_message(data):
  user = users.get(request.sid, None)
  if user:
    emit("new_message", {"username": user["username"], "message": data["message"]}, broadcast=True)

# This function will be called when the client updates the username
@socketio.on("update_username")
def handle_username(data):
  user = users.get(request.sid, None)
  if user:
    old_username = users[request.sid]["username"]
    user[request.sid]["username"] = data["username"]
    emit("update_username", {"old_username": old_username, "new_username": data["username"]}, broadcast=True)

if __name__ == '__main__':
  socketio.run(app)