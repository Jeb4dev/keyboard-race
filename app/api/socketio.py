from flask import request
from flask_socketio import emit, join_room, leave_room, close_room, SocketIO
from flask_jwt_extended import jwt_required
from random import choice
from datetime import datetime, timezone

from app.api.jwt import get_current_user
from app.models import Words, User
from app.models.db import db

"""
This file contains all server sockets.
"""

socketio = SocketIO(logger=True, cors_allowed_origins="*", async_mode="eventlet")

active_rooms = {}
users = {}


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
    # Update statistics object with new averages etc.
    print(data)
    if data["wpm"] > user.statistics.best_wpm:
        user.statistics.best_wpm = data["wpm"]
    else:
        user.statistics.best_wpm = user.statistics.best_wpm
    total_races = user.statistics.total_races + 1

    if data["ranking"] == 1:
        user.statistics.total_wins = user.statistics.total_wins + 1
    else:
        user.statistics.total_wins = user.statistics.total_wins

    # if it is users first race average records are same than current race records
    if total_races == 1:
        user.statistics.average_wpm = data["wpm"]

        user.statistics.average_epm = data["epm"]

        user.statistics.average_accuracy = data["accuracy"]

        user.statistics.average_time = data["time"]

    # else recalculate average values
    else:
        user.statistics.average_wpm = (user.statistics.average_wpm * (total_races - 1) + data.wpm) / total_races

        user.statistics.average_epm = (user.statistics.average_epm * (total_races - 1) + data.epm) / total_races

        user.statistics.average_accuracy = (user.statistics.average_accurasy * (
            total_races - 1) + data["accuracy"]) / total_races

        user.statistics.average_time = (user.statistics.average_time * (total_races - 1) + data.time) / total_races

    db.session.commit()

    print(f"{user.username} updated their statistics: word per minute was {data['wpm']}!")


def get_words():
    if len(Words.query.all()) < 1:
        db.session.add(Words(words="""One login. All your devices. A family of products that respect your privacy.
                                Join Firefox""", words_title="test", user_id=1))
        db.session.add(Words(words="""
                MR JONES of the Manor Farm, had locked the hen-houses for the night, but was too drunk to remember to shut the pop-holes. With the ring of light from his lantern dancing from side to side he lurched across the yard, kicked off his boots at the back door, drew himself a last glass of beer from the barrel in the scullery, and made his way up to bed, where Mrs Jones was already snoring.
                """, words_title="Animal Farm: C1 P1", user_id=1))
        db.session.add(Words(words="""
                As soon as the light in the bedroom went out there was a stirring and a fluttering all through the farm buildings. Word had gone round during the day that old Major, the prize Middle White boar, had had a strange dream on the previous night and wished to communicate it to the other animals. It had been agreed that they should all meet in the big barn as soon as Mr Jones was safely out of the way. Old Major (so he was always called, though the name under which he had been exhibited was Willingdon Beauty) was so highly regarded on the farm that everyone was quite ready to lose an hour's sleep in order to hear what he had to say.
                """, words_title="Animal Farm: C1 P2", user_id=1))
        db.session.add(Words(words="""
                At one end of the big barn, on a sort of raised platform, Major was already ensconced on his bed of straw, under a lantern which hung from a beam. He was twelve years old and had lately grown rather stout, but he was still a majestic-looking pig, with a wise and benevolent appearance in spite of the fact that his tushes had never been cut. Before long the other animals began to arrive and make themselves comfortable after their different fashions. First came the three dogs, Bluebell, Jessie and Pincher, and then the pigs, who settled down in the straw immediately in front of the platform. The hens perched themselves on the window-sills, the pigeons fluttered up to the rafters, the sheep and cows lay down behind the pigs and began to chew the cud. The two cart-horses, Boxer and Clover, came in together, walking very slowly and setting down their vast hairy hoofs with great care lest there should be some small animal concealed in the straw. Clover was a stout motherly mare approaching middle life, who had never quite got her figure back after her fourth foal. Boxer was an enormous beast, nearly eighteen hands high, and as strong as any two ordinary horses put together. A white stripe down his nose gave him a somewhat stupid appearance, and in fact he was not of first-rate intelligence, but he was universally respected for his steadiness of character and tremendous powers of work. After the horses came Muriel, the white goat, and Benjamin the donkey. Benjamin was the oldest animal on the farm, and the worst tempered. He seldom talked, and when he did it was usually to make some cynical remark — for instance he would say that God had given him a tail to keep the flies off, but that he would sooner have had no tail and no flies. Alone among the animals on the farm he never laughed. If asked why, he would say that he saw nothing to laugh at. Nevertheless, without openly admitting it, he was devoted to Boxer; the two of them usually spent their Sundays together in the small paddock beyond the orchard, grazing side by side and never speaking.
                """, words_title="Animal Farm: C1 P3", user_id=1))
        db.session.commit()
    return choice(Words.query.all()).to_dict(rules=('-id', '-user_id'))


# Error handling
@socketio.on_error()
@jwt_required()
def handle_error(e):
    print(f"An error occurred: {e}")


# When user connected
@socketio.on('connect')
@jwt_required()
def on_connect():
    user = get_current_user()
    print("User connected!", user)
    users[request.sid] = user.id


# When user disconnects
@socketio.on('disconnect')
def on_disconnect():
    user_id = users[request.sid]

    # Check if user was race leader, if -> remove lobby
    if active_rooms[user_id]:
        remove_room(user_id)
        del active_rooms[user_id]  # Does this work?
    # Iterate trough dict, check if user id in roomname.usernames, if -> leave room
    for owner_id, room in active_rooms.items():
        if user_id in room["username"]:
            # announce room that user left, if this is even needed
            emit('cl_user_left_race', user_id, to=owner_id)
            # Leave room
            leave_room(owner_id)
    print(f"{user_id} disconnected!")


# Create room
@socketio.on('sv_create_race')
@jwt_required()
def create_race():
    user = get_current_user()
    user_id = user.id

    room_title = f"{user.username}'s room"

    room_name = user_id

    # Check if room exist
    if room_name not in active_rooms:
        # Add room to dict of rooms
        active_rooms[user_id] = {
            "users": [],
            "room_title": room_title,
            "started": False,
            "words": get_words(),
            "time_start": 0
        }
    else:
        # Add user to room users list
        active_rooms[room_name]["users"].append(user_id)
    # Add room to dict of rooms

    # If the wordlist is empty, create one.

    emit('cl_create_race', active_rooms)  # must call sv_join_race
    print(f"{user.username} created {room_title} with id {user_id}!")


# Join room
@socketio.on('sv_join_race')
@jwt_required()
def join_race(data):
    user = get_current_user()

    room_name = data["room"]

    active_rooms[room_name]["users"].append(user.id)

    # Join room
    join_room(room_name)
    emit('cl_join_race')
    print(f"{user.username} joined {room_name}!")


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

    print(f"{user.username} left from {room_name}!")


# Get list of active rooms
@socketio.on('sv_get_active_rooms')
@jwt_required()
def list_active_races():
    user = get_current_user()

    # return active_rooms dictionary, that contains active_room_id, user_id's, room_title
    emit('sv_get_active_rooms', active_rooms)
    print(f"{user.username} asked list of active rooms! return {str(active_rooms)}")


# Start race
@socketio.on('sv_start_race')
@jwt_required()
def start_race():
    user = get_current_user()
    print("start")

    # Send word list to clients

    # Tell clients to start race
    active_rooms[user.id]["started"] = True
    active_rooms[user.id]["time_start"] = int(datetime.now(timezone.utc).timestamp() * 1000)
    emit('cl_start_race', to=user.id)
    print(f"{user.username} started race!")


# Clients send server race progress, that value is redirected all clients in the same race
@socketio.on('sv_get_progress')
@jwt_required()
def get_progress(data):  # data should at least contain room name, user whose data it is and what is the progress level
    user = get_current_user()
    words = Words.query.first()

    room_name = data["room"]

    # Tell clients to start race
    emit('cl_get_progress', data, to=room_name)

    print(f"{user.username} updated progress: {data['progress']}!")


# Get statistics when race is finished and save them to db, show user statistics
@socketio.on('sv_get_race_statistics')
@jwt_required()
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
