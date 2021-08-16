from flask import Flask, render_template, request, url_for, jsonify, session
from flask.helpers import send_from_directory
from flask_socketio import SocketIO, join_room,emit, rooms, send,close_room, join_room, leave_room
import random
import json
import os






class Player():
    def __init__ (self,playerName="unnamed",faceS = "face1", hairS = "hairS1", hairC = "hairC1", skin = "skin1", cloth = "cloth1", loc ="basement" ):
        self.playerName = playerName
        self.faceS = faceS
        self.hairS = hairS
        self.hairC = hairC
        self.skin = skin
        self.cloth = cloth
        self.loc = loc
    def return_path(self):
        return self.skin+"_"+self.hairC+"_"+self.cloth+"_"+self.hairS+"_"+self.faceS

Player_list_by_sid = []
Player_list_by_name = []
first_floor_player = []
basement_floor_player = []
second_floor_player = []

app = Flask(__name__)
app.secret_key = "cuberoom"
socketio = SocketIO(app)




@app.route("/")
def base():
    return send_from_directory('cuberoom-main/public','index.html')


@app.route("/<path:path>")
def home(path):
    return send_from_directory('cuberoom-main/public',path)



@app.route("/character-selection",methods=['POST'])
def user_information():
    name = request.form['name']
    names  = name.split('.')
    faceS = request.get_json("faceS")
    hairS = request.get_json("hairS")
    hairC = request.get_json("hairC")
    skin =  request.get_json("skin")
    cloth = request.get_json("cloth")
    #faceS,hairS,hairC,skin,cloth = request.form.getlist('')
    if Player_list_by_name[name] is not None:
        return 0;
    Player_list_by_sid[request.sid] = Player(name,faceS,hairS,hairC,skin,cloth)
    Player_list_by_name[name] = request.sid
    filePath = "/faceS"+faceS+"_hairS"+hairS+"_hairC"+hairC+"_hairS"+hairS+"_skin"+skin+"_cloth"+cloth+"/"
   ##return jsonify(faceS = request.get_json("faceS"),
   ##                 hairS = request.get_json("hairS"),
   ##                 hairC = request.get_json("hairC"),
   ##                 skin =  request.get_json("skin"),
   ##                 cloth = request.get_json("cloth"),)
    return  filePath

@app.route("./game")
def foo():
    return 0

@socketio.on('change_loaction','character-generator')
def user_information(data):
    username = data['username']
    Player_list_by_sid['name'].loc = data['cur_loc']
    previous_room = data['prev_loc']
    leave_room(previous_room)
    change_data = {
        'name' : username,
        'faceS' : Player_list_by_sid['faceS'].faceS,
        'hairsS' : Player_list_by_sid['hairS'].hairS,
        'hairC' : Player_list_by_sid['hairC'].hairC,
        'skin' : Player_list_by_sid['skin'].skin,
        'cloth' : Player_list_by_sid['cloth'].cloth,
        'loc' : Player_list_by_sid['cur_loc'].loc,
    }
    session['room'] = change_data['loc']
    new_room = session.get('room')
    join_room(new_room)
    name_space = '/'+ data['loc']
    emit("change_response",change_data,name_space)



@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('connection','/entrance')
def message(data):
    emit("response",data,namespace = './entrance')

@socketio.on('connection','/basement')
def message(data):
    emit("response",data,namespace = './basement')

@socketio.on('connection','/firstFloor')
def message(data):
    emit("response",data,namespace = '/firstFloor')

@socketio.on('connection','/secondFloor')
def message(data):
    emit("response",data,namespace = '/secondFloor')



if __name__ == "__main__":
    app.run(debug=True)