#wsgi.py

from flask import Flask, render_template, request, url_for, jsonify, session
from flask.helpers import send_from_directory
from flask_socketio import SocketIO, join_room,emit, rooms, send,close_room, join_room, leave_room
import random
import json
import os






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


app = Flask(__name__)
app.secret_key = "cuberoom"
socketio = SocketIO(app)




@app.route("/")
def base():
    return send_from_directory('cuberoom/public','index.html')


@app.route("/<path:path>")
def home(path):
    return send_from_directory('cuberoom/public',path)



# @app.route("/character-selection",methods=['POST'])
# def user_information():
#     name = request.form['name']
#     names  = name.split('.')
#     faceS = request.get_json("faceS")
#     hairS = request.get_json("hairS")
#     hairC = request.get_json("hairC")
#     skin =  request.get_json("skin")
#     cloth = request.get_json("cloth")
#     #faceS,hairS,hairC,skin,cloth = request.form.getlist('')
#     if Player_list_by_name[name] is not None:
#         return 0;
#     Player_list_by_sid[request.sid] = Player(name,faceS,hairS,hairC,skin,cloth)
#     Player_list_by_name[name] = request.sid
#     filePath = "/faceS"+faceS+"_hairS"+hairS+"_hairC"+hairC+"_hairS"+hairS+"_skin"+skin+"_cloth"+cloth+"/"
#    ##return jsonify(faceS = request.get_json("faceS"),
#    ##                 hairS = request.get_json("hairS"),
#    ##                 hairC = request.get_json("hairC"),
#    ##                 skin =  request.get_json("skin"),
#    ##                 cloth = request.get_json("cloth"),)
#     return  filePath





# #########################################################################################
# @socketio.on('text', namespace='/chat')
# def text(message):
#     """Sent by a client when the user entered a new message.
#     The message is sent to all people in the room."""
#     room = session.get('room')
#     emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)
# #########################################################################################

# @socketio.on('entrance_connection','/entrance')
# def message(data):
#     emit("entrance_response",data,namespace = './entrance',broadcast = True)

# @socketio.on('1F_connection','/1F')
# def message(data):
#     Player_list_by_sid[data['id']]
#     emit("1F_response",data,namespace = '/1F',broadcast = True)

# @socketio.on('2F_connection','/2F')
# def message(data):
#     emit("2F_response",data,namespace = '/2F',broadcast = True)

# # @socketio.on('3F_connection','/3F')
# # def message(data):
# #     emit("3F_response",data,namespace = '/3F',broadcast = True)

# @socketio.on('5F_connection','/5F')
# def message(data):
#     emit("5F_response",data,namespace = '/5F',broadcast = True)

# @socketio.on('6F_connection','/6F')
# def message(data):
#     emit("6F_response",data,namespace = '/6F',broadcast = True)

# @socketio.on('7F_connection','/7F')
# def message(data):
#     emit("7F_response",data,namespace = '/7F',broadcast = True)

# @socketio.on('8F_connection','/8F')
# def message(data):
#     emit("8F_response",data,namespace = '/8F',broadcast = True)

# @socketio.on('1B_connection','/1B')
# def message(data):
#     emit("1B_response",data,namespace = '/1B',broadcast = True)

# @socketio.on('2B_connection','/2B')
# def message(data):
#     emit("2B_response",data,namespace = '/2B',broadcast = True)


####generating character######################
#   from client
#   data = {
#       'name'     
#  }
#################################################
@socketio.on('namecheck')
def namecheck(data):
    if Player_list_by_name[data['name']] is not None:
        session['usrname'] = data['name']
        send('namecheck',{'valid' : 1})
    else 
        send('namecheck',{'valid' : 0})

####generating character######################
#   from client
#   data = {
#       'name'     
#       'avatar_path'
#  }
#################################################
@socketio.on('connection')
def connect(data):
    total_player +=1
    p = Player(data['name'],data['avatar_path'],'entrance')
    Player_list_by_name[data['name']] = p
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
#       
#       'cur_loc'(현재위치 )
#       'next_loc' (이동하고자하는 위치)
#  
#   }
##############################################
@socketio.on('change_loaction')
def user_information(data):
    username = session['usrname']

    change_data = {
        'avatar_path' : Player_list_by_name[username].avatar_path,
        'loc' : data['next_loc']
    }
    name_space = '/'+ data['next_loc']
    emit("change_location",change_data, namespace = name_space)


############################################
#   from client
#   data = {
#       'name'     
#       'cur_loc'(현재위치 )
#       'next_loc' (이동하고자하는 위치)
#  
#   }
##############################################
@socektio.on('addChat')
def add_chat(data):
    loc = data['loc']
    chat_namespace = '/'+loc
    Player_list_by_name[data['name']]

    emit('addChat',{'player_name' : session['name'],'msg' : data['msg']},namespace = chat_namespace, broadcast = True)


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
    loc = data['loc']
    chat_namespace = '/' + loc
    emit('removeChat',{'name' : data['name'], 'msg': ''},namespace =chat_namespace, broadcast = True)



############################################
#   from client
#   data = {
#       x
#       y
#       
#   }
##############################################
@socketio.on("player_movement")
def update_move(data):
    response_message = {
        'player_name' : ,
        'filePath' : ,
        'x' : x,
        'y' : y,
        'loc' :
    }

    emit('player_movement',response_message,broadcast =True)


############################################
#   from client
#   data = {
#       'name'     
#       'cur_loc'(현재위치 )
#       'next_loc' (이동하고자하는 위치)
#  
#   }
##############################################
@socketio.on("disconnect")
def disconnect(data):
    del Player_list_by_name[data['name']]
    del floor_player_list[data['loc']][data['name']]
    total_player -=1
    emit('disconnect',broadcast =True)

if __name__ == "__main__":
    app.run(debug=True)