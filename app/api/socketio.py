from flask_socketio import emit, join_room, leave_room, close_room, SocketIO
from flask_jwt_extended import jwt_required

from app.api.jwt import get_current_user
from app.models import Words
from app.models.db import db

"""
This file contains all server sockets.
"""

socketio = SocketIO(logger=True, cors_allowed_origins="*", async_mode="eventlet")

active_rooms = {}


# TODO: error handling, expired token, wrong / missing data

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
    # TODO: check if this works
    # Update statistics object with new averages etc.
    if data.wpm > user.statistics.best_wpm:
        user.statistics.best_wpm = data.wpm
    else:
        user.statistics.best_wpm = user.statistics.best_wpm
    total_races = user.statistics.total_races + 1

    if data.ranking == 1:
        user.statistics.total_wins = user.statistics.total_wins + 1
    else:
        user.statistics.total_wins = user.statistics.total_wins

    # if it is users first race average records are same than current race records
    if total_races == 1:
        user.statistics.average_wpm = data.wpm

        user.statistics.average_epm = data.epm

        user.statistics.average_accuracy = data.accuracy

        user.statistics.average_time = data.time

    # else recalculate average values
    else:
        user.statistics.average_wpm = (user.statistics.average_wpm * (total_races - 1) + data.wpm) / total_races

        user.statistics.average_epm = (user.statistics.average_epm * (total_races - 1) + data.epm) / total_races

        user.statistics.average_accuracy = (user.statistics.average_accurasy * (
            total_races - 1) + data.accuracy) / total_races

        user.statistics.average_time = (user.statistics.average_time * (total_races - 1) + data.time) / total_races

    db.session.commit()

    print(f"{user.username} updated their statistics: word per minute was {data['wpm']}!")


# When user connected
@socketio.on('connect')
@jwt_required()
def on_connect():
    print("User connected!")


# When user disconnects
@socketio.on('disconnect')
def on_disconnect():
    print("Unknown user disconnected!")
    return True
    # TODO: ISSUE: get_current_user() returns error as user is no more current... ?
    user = get_current_user()  # This doesnt work

    # Check if user was race leader, if -> remove lobby
    if active_rooms[user.id]:
        remove_room(user.id)
        del active_rooms[user.id]  # Does this work?
    # Iterate trough dict, check if user id in roomname.usernames, if -> leave room
    for owner_id, room in active_rooms.items():
        if user.id in room["username"]:
            # announce room that user left, if this is even needed
            emit('cl_user_left_race', user.id, to=owner_id)
            # Leave room
            leave_room(owner_id)
    print(f"{user.username} disconnected!")


# Create room
@socketio.on('sv_create_race')
@jwt_required()
def create_race(data):
    user = get_current_user()
    user_id = user.id

    room_title = f"{user.username}'s room"

    room_name = user_id

    # Check if room exist
    if room_name not in active_rooms:
        # Add room to dict of rooms
        active_rooms[user_id] = {
            "users": [user_id],
            "room_title": room_title
        }
    else:
        # Add user to room users list
        active_rooms[room_name]["users"].append(user_id)
    # Add room to dict of rooms
    active_rooms[user_id] = {
        "users": [],
        "room_title": room_title
    }

    # If the wordlist is empty, create one.
    if len(Words.query.all()) < 1:
        words_ = Words(words="""One login. All your devices. A family of products that respect your privacy.
                        Join Firefox""", words_title="test", user_id=user.id)
        db.session.add(words_)
        db.session.commit()
        print("Created new record in Words table")

    emit('cl_create_race', user_id)  # must call sv_join_race
    print(f"{user.username} created {room_title} with id {user_id}!")


# Join room
@socketio.on('sv_join_race')
@jwt_required()
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
@jwt_required()
def leave_race(data):
    user = get_current_user()
    user_id = user.id

    room_name = data["room"]

    # announce room that user left, if this is even needed
    emit('cl_user_left_race', user_id, to=room_name)

    # Leave room
    leave_room(room_name)

    # Remove user from room dict
    active_rooms[room_name]["users"].remove(user.id)

    # if user was creator of room, -> delete room
    if active_rooms[user.id]:
        remove_room(user.id)
        del active_rooms[user.id]

    print(f"{user.username} left {data['room_title']}!")


# Get list of active rooms
@socketio.on('sv_get_active_rooms')
@jwt_required()
def list_active_races(data):
    user = get_current_user()

    # return active_rooms dictionary, that contains active_room_id, user_id's, room_title
    emit('sv_get_active_rooms', active_rooms)
    print(f"{user.username} asked list of active rooms! return {str(active_rooms)}")


# Start race
@socketio.on('sv_start_race')
@jwt_required()
def start_race(data):
    user = get_current_user()

    room_name = data["room"]
    room_title = active_rooms[room_name]["room_title"]

    # Send word list to clients
    words = Words.query.first()
    wordlist_title = words.words_title
    wordlist = words.words
    emit('cl_get_wordlist', (wordlist_title, wordlist), to=room_name)

    # Tell clients to start race
    emit('cl_start_race', data, to=room_name)
    print(f"{user.username} started race in {room_title}!")


# Clients send server race progress, that value is redirected all clients in the same race
@socketio.on('sv_get_progress')
@jwt_required()
def get_progress(data):  # data should at least contain room name, user whose data it is and what is the progress level
    user = get_current_user()
    words = Words.query.first()

    room_name = data["room"]

    words_title = words.words_title
    wordlist = words.words

    # Send word list to clients
    emit('cl_get_wordlist', (words_title, wordlist), to=room_name)

    # Tell clients to start race
    emit('cl_get_progress', data, to=room_name)

    print(f"{user.username} updated progress: {data['progress']}!")


# Get statistics when race is finished and save them to db, show user statistics
@socketio.on('sv_get_race_statistics')
@jwt_required()
def get_race_statistics(data):
    # TODO: test if this socket work as intended, also if function handle_statistics() work.
    # data should at least contain: room name, wpm, epm, ranking,
    # total participants, accuracy, race time, words title, errors

    user = get_current_user()

    # save statistics to db
    handle_statistics(user, data)

    # call event when statistics are updated
    # on this event client can show all statistics of recent race and updated statistics of all time
    # at the same graph or what ever you decide to show statistics...
    emit('show statistics')
