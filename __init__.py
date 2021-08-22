from flask import Flask, render_template, request, url_for, jsonify, session
from flask.helpers import send_from_directory
from flask_socketio import SocketIO, join_room,emit, rooms, send,close_room, join_room, leave_room
import random
import json
import os
from flask_cors import CORS






class Player():
    def __init__ (self,playerName="unnamed", avatar_path="",loc ="basement",x = 16*6, y = 16*11): #faceS = "face1", hairS = "hairS1", hairC = "hairC1", skin = "skin1", cloth = "cloth1"
        avatar =  avatar_path.split('_')
        self.playerName = playerName
        # self.faceS = faceS
        # self.hairS = hairS
        # self.hairC = hairC
        # self.skin = skin
        # self.cloth = cloth
        self.avatar_path = avatar_path
        self.loc = loc
        self.x = x
        self.y = y


Player_list_by_sid = {}
Player_list_by_name = {}
floor_player_list = {
    "entrance" : {},
    "1B": {},
    "2B": {},
    "1F": {},
    "2F": {},
    "5F": {},
    "6F": {},
    "7F": {},
    "8F": {},
    "9F": {},
}
total_player = 0

app = Flask(__name__)#, static_url_path='/static/public', static_folder='')
#CORS(app, resources={r'*': {'origins': 'http://localhost:5000'}})
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
    name = request.get_json()["username"]
    faceS = request.get_json()["faceS"]
    hairS = request.get_json()["hairS"]
    hairC = request.get_json()["hairC"]
    skin =  request.get_json()["skin"]
    cloth = request.get_json()["cloth"]

    # name =  request.get_json("username") 
    # faceS = request.get_json("faceS")
    # hairS = request.get_json("hairS")
    # hairC = request.get_json("hairC")
    # skin =  request.get_json("skin")
    # cloth = request.get_json("cloth")

    # session['username'] = name
    # session['room'] = "basement"
    # if Player_list_by_name[name] is not None:
    #     return 0;
    # Player_list_by_sid[request.sid] = Player(name,faceS,hairS,hairC,skin,cloth)
    # Player_list_by_name[name] = request.sid
    Player_list_by_name[name] = Player(name,filePath)
    filePath = f"results/skin{skin}_hairC{hairC}_cloth{cloth}_hairS{hairS}_faceS{faceS}/"
    print(filePath)
    return url_for('static',filename = filePath)




@socketio.on('namecheck')
def namecheck(data):
    if Player_list_by_name[data['name']] is not None:
        session['usrname'] = data['name']
        send('namecheck',{'valid' : 1})
    else 
        send('namecheck',{'valid' : 0})


@socketio.on('connection')
def connect(data):
    total_player +=1
    p = Player(data['name'],data['avatar_path'],'entrance')
    Player_list_by_name[data['name']] = p
    Player_list_by_sid[data['id']] = p
    floor_player_list['entrance'][data['name']] = p
    player_info = {
        'name' : p.playerName,
        'avatar_path' : p.avatar_path,
        'loc' : p.loc,
        'x' : p.x,
        'y' : p.y
    }
    emit('connection',player_info, namespace = '/entrance', broadcast = True)






############################################
#   from client
#   data = {
#       'id'     
#       'cur_loc'(현재위치 )
#       'next_loc'
#  
#   }
##############################################
@socketio.on('change_loaction')
def user_information(data):
    username = Player_list_by_sid[data['id']]
    cur_loc = data['cur_loc']
    next_loc = data['next_loc']
    change_data = {
        'avatar_path' : Player_list_by_name[username].avatar_path,
        'loc' : data['next_loc']
        'x' :16*5, 
        'y' 16*31:
    }
    
    Player_list_by_name[username].x = 16*5
    Player_list_by_name[username].y = 16*31
    Player_list_by_name[username].loc = next_loc

    Player_list_by_sid[data['id']].x = 16*5
    Player_list_by_sid[data['id']].y = 16*31
    Player_list_by_sid[data['id']].loc = next_loc

    floor_player_list[next_loc][username] = Player_list_by_sid[data['id']]
    del floor_player_list[cur_loc][username]
    name_space = '/'+ data['next_loc']
    emit("change_location",change_data, namespace = name_space)


############################################
#   from client
#   data = {
#       'name'     
#       'cur_loc'(현재위치 )
#       
#  
#   }
##############################################
@socektio.on('addChat')
def add_chat(data):
    chat_namespace = '/'+Player_list_by_sid[data['id']].loc
    usrname = Player_list_by_sid[data['id']].username

    emit('addChat',{'player_name' : usrname,'msg' : data['msg']},namespace = chat_namespace, broadcast = True)


############################################
#   from client
#   data = {
#       'name'     
#       'cur_loc'(현재위치 )
#       'next_loc' (이동하고자하는 위치)
#  
#   }
##############################################
@socketio.on("removeChat")
def remove_chat(data):
    loc = Player_list_by_sid[data['id']].loc
    chat_namespace = '/' + loc
    emit('removeChat',{'name' : data['id'], 'msg': ''},namespace =chat_namespace, broadcast = True)



############################################
#   from client
#   data = {
#       id
#       x
#       y
#       
#   }
##############################################
@socketio.on("player_movement")
def update_move(data):

    response_message = {
        'player_name' : Player_list_by_sid[data['id']].username,
        'filePath' : Player_list_by_sid[data['id']].avatar_path
        'x' : data['x'],
        'y' : data['y'],
        'loc' : Player_list_by_sid[data['id']].loc
    }
    Player_list_by_name[username].x =  data['x']
    Player_list_by_name[username].y = data['y']
    

    Player_list_by_sid[data['id']].x =  data['x']
    Player_list_by_sid[data['id']].y = data['y']

    emit('player_movement',response_message,broadcast =True)


############################################
#   from client
#   data = {
#       'id'     
#  
#   }
##############################################
@socketio.on("disconnect")
def disconnect(data):
    usrname = Player_list_by_sid[data['id']].username
    loc = Player_list_by_sid[data['id']].loc
    
    del Player_list_by_name[usrname]

    del floor_player_list[loc][usrname]
    total_player -=1

    del Player_list_by_sid[data['id']]

    emit('disconnect',{'id':data['id']},broadcast =True)


if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, port=5000)