import config

import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
socketio = SocketIO(app)

rooms = {}

from app import routes
from app import events
