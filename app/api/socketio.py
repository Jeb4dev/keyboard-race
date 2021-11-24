from flask_socketio import emit, join_room, leave_room, close_room
from app.app import socketio
from app.api.jwt import get_current_user
from app.models import Words


"""
This file contains all server sockets.
"""


active_rooms = {}


# Redirect users to landing page
# Close / remove room
def remove_room(room_name):

    # will users disconnect automatically when room is closed or do we need to use "leave_room()" ?

    # Should users in room be redirected somewhere before close?? ↓ ↓
    emit('cl_on_room_close', to=room_name)  # This will redirect users to landing page etc...

    # Close room
    close_room(room_name)
    # Is this same than removing room, will it behave like it never existed??


# Handle saving statistics to the database
def handle_statistics(user, data):
    # TODO: saving changes to db...
    # TODO: calculating new averages...
    print(f"{user.username} updated their statistics: word per minute was {data['wpm']}!")


# When user connected
@socketio.on('connect')
def on_connect():
    emit("connect")
    print("User connected!")


# When user disconnects
@socketio.on('disconnect')
def on_disconnect():
    user = get_current_user()

    # Check if user was race leader, if -> remove lobby
    if active_rooms[user.id]:
        remove_room(user.id)
        active_rooms[user.id].clear()  # Does this work?
    # Iterate trough dict, check if user id in roomname.usernames, if -> leave room
    for key in active_rooms:
        if user.id in key["username"]:
            # announce room that user left, if this is even needed
            emit('cl_user_left_race', user.id, to=key)
            # Leave room
            leave_room(key)
    print(f"{user.username} disconnected!")


# Create room
@socketio.on('sv_create_race')
def create_race(data):
    user = get_current_user()
    user_id = user.id

    room_title = f"{user.username}'s room"

    if data["room"]:
        room_name = data["room"]
    else:
        room_name = user_id

    # Add room to dict of rooms
    active_rooms[user_id] = {
        "users": [],
        "room_title": room_title
        }

    emit('cl_create_race', room_title)  # must call sv_join_race
    print(f"{user.username} created {room_title}!")


# Join room
@socketio.on('sv_join_race')
def join_race(data):
    user = get_current_user()

    room_title = data["room_title"]

    room_name = data["room"]

    active_rooms[room_name]["users"].append(user.id)

    # Join room
    join_room(room_name)
    emit('cl_join_race', room_title)
    print(f"{user.username} joined {room_title}!")


# Leave room
@socketio.on('sv_leave_race')
def leave_race(data):
    user = get_current_user()
    user_id = user.id

    room_name = data["room"]

    # announce room that user left, if this is even needed
    emit('cl_user_left_race', user_id, to=room_name)
    # Leave room
    leave_room(room_name)
    print(f"{user.username} left {data['room_title']}!")


# Get list of active rooms
@socketio.on('sv_get_active_rooms')
def list_active_races(data):
    user = get_current_user()

    # return active_rooms dictionary, that contains active_room_id, user_id's, room_title
    emit('sv_get_active_rooms', active_rooms)
    print(f"{user.username} asked list of active rooms! return {str(active_rooms)}")


# Start race
@socketio.on('sv_start_race')
def start_race(data):
    user = get_current_user()

    room_name = data["room"]
    room_title = active_rooms[room_name]["room_title"]

    # Send word list to clients
    wordlist_title = ""
    wordlist = ""
    emit('cl_get_wordlist', wordlist_title, wordlist, to=room_name)

    # Tell clients to start race
    emit('cl_start_race', data, to=room_name)
    print(f"{user.username} started race in {room_title}!")


# Clients send server race progress, that value is redirected all clients in the same race
@socketio.on('sv_get_progress')
def get_progress(data):  # data should at least contain room name, user whose data it is and what is the progress level
    user = get_current_user()
    words = Words.query.all()

    room_name = data["room"]

    words_title = words.words_title
    wordlist = words.words

    # Send word list to clients
    emit('cl_get_wordlist', words_title, wordlist, to=room_name)

    # Tell clients to start race
    emit('cl_get_progress', data, to=room_name)

    print(f"{user.username} updated progress: {data['progress']}!")


# Get statistics when race is finished and save them to db, show user statistics
@socketio.on('sv_get_race_statistics')
def get_race_statistics(data):
    # data should at least contain: room name, wpm, epm, ranking,
    # total participants, accuracy, race time, words title, errors

    user = get_current_user()

    # save statistics to db
    handle_statistics(user, data)

    # call event when statistics are updated
    # on this event client can show all statistics of recent race and updated statistics of all time
    # at the same graph or what ever you decide to show statistics...
    emit('show statistics')
