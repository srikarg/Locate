from flask import session
from flask_socketio import emit, join_room, leave_room
from . import socketio
from app import rooms

@socketio.on('joined')
def joined(data):
    user = session['username']
    room = session['room_id']
    print '{} joined room {}'.format(user, room)
    join_room(room)
    if room not in rooms:
        rooms[room] = { 'users': {} }
    rooms[room]['users'][user] = {}
    user_list = sorted(rooms[room]['users'].keys())
    emit('list of users', { 'users': user_list }, room=room)

@socketio.on('left')
def left(data):
    user = session['username']
    room = session['room_id']
    print '{} left room {}'.format(user, room)
    leave_room(room)
    if user in rooms[room]['users']:
        rooms[room]['users'].pop(user, None)
    user_list = sorted(rooms[room]['users'].keys())
    emit('list of users', { 'users': user_list }, room=room)
    emit('update locations', { 'userData': rooms[room]['users'] }, room=room)

@socketio.on('new location')
def new_location(data):
    user = session['username']
    room = session['room_id']
    if user in rooms[room]['users']:
        rooms[room]['users'][user] = { 'lat': data['position'][0], 'lng': data['position'][1] }
    emit('update locations', { 'userData': rooms[room]['users'] }, room=room)
