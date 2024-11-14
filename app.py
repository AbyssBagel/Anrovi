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

# This function will be called when the client connect to the server
@socketio.on("connect")
def handle_connect():
  username = f"User_{random.randint(1000, 9999)}" # This is a random username
  private_key = random.randint(100000, 999999) # This is a private key that will be used to encrypt the message

  users[request.sid] = {"username": username, "private_key": private_key}

  emit("connected", {"username": username}, broadcast=True)

  emit("set_username", {"username": username})

if __name__ == '__main__':
  socketio.run(app)