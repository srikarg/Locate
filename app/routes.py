from flask import flash, render_template, request, redirect, url_for, session
from app import app, rooms

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], room=session['room_id'])
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        room = request.form['roomid']
        if username.isspace() != True and room.isspace() != True and username != '' and room != '':
            if room in rooms:
                if username in rooms[room]['users']:
                    flash('{} is already in {}! Please choose another username or room.'.format(username, room))
                    return redirect(url_for('index'))
            session['username'] = username
            session['room_id'] = room
            return redirect(url_for('room', room_id=room))

@app.route('/room/<room_id>')
def room(room_id):
    if 'username' not in session:
        return redirect('/')
    else:
        session['room_id'] = room_id
        return render_template('room.html', user=session['username'], room=room_id)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('index'))
