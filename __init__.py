from flask import Flask, render_template, request, url_for, jsonify, session
from flask.helpers import send_from_directory
from flask_socketio import SocketIO, emit, rooms, send, close_room, join_room, leave_room
import random
import json
import os
from flask_cors import CORS

# Player_list_by_sid = {}
# Player_list_by_name = {}
# first_floor_player = {}
# basement_floor_player = {}
# second_floor_player = {}

app = Flask(__name__, static_url_path='', static_folder='')
CORS(app, resources={r'*': {'origins': 'http://localhost:5000'}})

app.secret_key = "cuberoom"
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def base():
    return send_from_directory('cuberoom-main/public','index.html')

@app.route("/<path:path>", methods=['GET', 'POST'])
def home(path):
    return send_from_directory('public', path)

@app.route("/character-selection",methods=['GET', 'POST'])
def user_information():
    name = request.get_json()["name"]
    faceS = request.get_json()["faceS"]
    hairS = request.get_json()["hairS"]
    hairC = request.get_json()["hairC"]
    skin =  request.get_json()["skin"]
    cloth = request.get_json()["cloth"]

    # session['username'] = name
    # session['room'] = "basement"
    # if Player_list_by_name[name] is not None:
    #     return 0;
    # Player_list_by_sid[request.sid] = Player(name,faceS,hairS,hairC,skin,cloth)
    # Player_list_by_name[name] = request.sid

    filePath = f"/skin{skin}_hairC{hairC}_cloth{cloth}_hairS{hairS}_faceS{faceS}/"
    return url_for('static', filename=filePath)

# @app.route("/game")
# def foo():
#     return 0

# @socketio.on('change_loaction','character-generator')
# def user_information(data):
#     username = data['username']
#     Player_list_by_sid['name'].loc = data['cur_loc']
#     previous_room = data['prev_loc']
#     leave_room(previous_room)
#     change_data = {
#         'name' : username,
#         'faceS' : Player_list_by_sid['faceS'].faceS,
#         'hairsS' : Player_list_by_sid['hairS'].hairS,
#         'hairC' : Player_list_by_sid['hairC'].hairC,
#         'skin' : Player_list_by_sid['skin'].skin,
#         'cloth' : Player_list_by_sid['cloth'].cloth,
#         'loc' : Player_list_by_sid['cur_loc'].loc,
#     }
#     session['room'] = change_data['loc']
#     new_room = session.get('room')
#     # join_room(new_room)
#     name_space = '/'+ data['cur_loc']
#     emit("change_response",change_data,name_space)


players = {}

class Player():
    def __init__ (self, id, name, imgUrl, floor, x, y):
        self.id = id
        self.name = name
        self.imgUrl = imgUrl
        self.floor = floor
        self.x = x
        self.y = y
        self.chat = ''
        self.direction = 'down'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'imgUrl': self.imgUrl,
            'floor': self.floor,
            'x': self.x,
            'y': self.y,
            'chat': self.chat,
            'direction': self.direction,
        }

@socketio.on('addPlayer')
def addPlayer(data):
    global players
    player = Player(data['id'], data['name'], data['imgUrl'], data['floor'], data['x'], data['y'])
    players[data['id']] = player.serialize()
    join_room(player.floor)
    # emit('addPlayer', {
    #     'id': player.id,
    #     'name': player.name,
    #     'imgUrl': player.imgUrl,
    #     'floor': player.floor,
    #     'x': player.x,
    #     'y': player.y,
    #     'chat': player.chat,
    #     'direction': player.direction,
    # }, broadcast=True)
    emit('playerList', players, broadcast=True, to=data['floor'])

@socketio.on('moveFloor')
def moveFloor(data):
    global players
    prevRoom = players[data['id']]['floor']
    nextRoom = data['floor']
    players[data['id']]['floor'] = nextRoom
    leave_room(prevRoom)
    join_room(nextRoom)
    emit('removePlayer', { 'id': data['id'] }, to=prevRoom)
    emit('playerList', players, to=nextRoom)

@socketio.on('addChat')
def addChat(data):
    global players
    players[data['id']]['chat'] = data['chat']
    emit('addChat', data, broadcast=True, to=players[data['id']]['floor'])

@socketio.on('removeChat')
def removeChat(data):
    global players
    players[data['id']]['chat'] = ''
    emit('removeChat', data, broadcast=True, to=players[data['id']]['floor'])

@socketio.on('movePlayer')
def movePlayer(data):
    global players
    if data['id'] in players.keys():
        players[data['id']]['x'] = data['x']
        players[data['id']]['y'] = data['y']
        players[data['id']]['direction'] = data['direction']
        emit('playerList', players, broadcast=True, to=data['floor'])

@socketio.on('disconnect')
def disconnect():
    global players
    players.pop(request.sid, None)
    emit('removePlayer', { 'id': request.sid })

# @socketio.on('connection','/entrance')
# def message(data):
#     emit("response",data,namespace = './entrance')

# @socketio.on('connection','/basement')
# def message(data):
#     emit("response",data,namespace = './basement')

# @socketio.on('connection','/firstFloor')
# def message(data):
#     emit("response",data,namespace = '/firstFloor')

# @socketio.on('connection','/secondFloor')
# def message(data):
#     emit("response",data,namespace = '/secondFloor')

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True, port=3000)
