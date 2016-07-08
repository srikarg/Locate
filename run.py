#!flask/bin/python -B
from app import app, socketio
socketio.run(app, debug=False)
