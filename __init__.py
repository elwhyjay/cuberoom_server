from flask import Flask, request, url_for
from flask.helpers import send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import time


app = Flask(__name__)#, static_url_path='', static_folder='')
CORS(app, resources={r'*': {'origins': 'http://cuberoom.net'}})

app.secret_key = "cuberoom"
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route("/")
def base():
    return send_from_directory('cuberoom/public','index.html')

@app.route("/<path:path>", methods=['GET', 'POST'])
def home(path):
    return send_from_directory('cuberoom/public', path)


@app.route("/character-selection",methods=['GET', 'POST'])
def user_information():
    name = request.get_json()["name"]
    faceS = request.get_json()["faceS"]
    hairS = request.get_json()["hairS"]
    hairC = request.get_json()["hairC"]
    skin =  request.get_json()["skin"]
    cloth = request.get_json()["cloth"]

    filePath = f"results/skin{skin}_hairC{hairC}_cloth{cloth}_hairS{hairS}_faceS{faceS}/"
    return url_for('static',filename = filePath)


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
    time.sleep(0.5)
    emit('playerList', players, broadcast=True, to=data['floor'])

@socketio.on('moveFloor')
def moveFloor(data):
    global players
    prevRoom = players[data['id']]['floor']
    nextRoom = data['floor']
    players[data['id']]['floor'] = nextRoom
    leave_room(prevRoom)
    join_room(nextRoom)
    emit('removePlayer', { 'id': data['id'] }, broadcast=True, to=prevRoom)
    time.sleep(1)
    emit('playerList', players, broadcast=True, to=nextRoom)

@socketio.on('addChat')
def addChat(data):
    global players
    players[data['id']]['chat'] = data['chat']
    # emit('addChat', data, broadcast=True, to=players[data['id']]['floor'])
    emit(
        'addChat',
        {
            'id': data['id'],
            'chat': data['chat'],
            'floor': players[data['id']]['floor'],
        },
        broadcast=True,
        to=players[data['id']]['floor']
    )

@socketio.on('removeChat')
def removeChat(data):
    global players
    players[data['id']]['chat'] = ''
    # emit('removeChat', data, broadcast=True, to=players[data['id']]['floor'])
    emit(
        'removeChat',
        {
            'id': data['id'],
            'chat': '',
            'floor': players[data['id']]['floor'],
        },
        broadcast=True,
        to=players[data['id']]['floor']
    )

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

if __name__ == "__main__":
    socketio.run(app, debug=True)
