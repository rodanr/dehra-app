from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
from db import *

app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/')
def home():
    # Inital Page
    return render_template("index.html")

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))

@socketio.on('joined_room')
def handle_join_room_event(data):
    # app.logger.info("{} has joined the room {}.". format(data["username"], data['room']))
    cur.execute("""INSERT INTO users(username, room_id)
        VALUES (%(str)s, %(int)s)""", {'str': data['username'], 'int': data['room']})
    conn.commit()
    cur.execute("SELECT id, username, messages FROM message WHERE room_id = %s",(data['room'],))
    value = cur.fetchall()
    join_room(data['room'])
    if value is not None:
        socketio.emit('rejoin_room', value,room=data["room"])
    socketio.emit('join_room_announcement', data, room = data["room"], broadcast=True, include_self=False)

@socketio.on('send_message')
def handle_send_messsage_event(data):
    cur.execute("""INSERT INTO message (room_id, username, messages)
        VALUES (%(room)s, %(username)s, %(message)s);
        """,{'room': data['room'], 'username': data['username'],'message': data['message']})
    conn.commit()
    app.logger.info("{} has sent message to the room {}: {}". format(data["username"], data['room'], data["message"]))
    socketio.emit('recieve_message', data, room=data['room'])

@socketio.on('typing_status')
def typing_status_handler(data):
    socketio.emit('typing_on',data ,broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)