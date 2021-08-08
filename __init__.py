from flask import Flask, render_template, request, url_for, jsonify
from flask.helpers import send_from_directory
from flask_socketio import SocketIO, join_room,emit, rooms, send,close_room
import random
import json
import os

Player_list = {}
class Player():
    def __init__ (self,playerName="unnamed",faceS = "face1", hairS = "hairS1", hairC = "hairC1", skin = "skin1", cloth = "cloth1" ):
        self.playerName = playerName
        self.faceS = faceS
        self.hairS = hairS
        self.hairC = hairC
        self.skin = skin
        self.cloth = cloth
    
    def return_path(self):
        return self.skin+"_"+self.hairC+"_"+self.cloth+"_"+self.hairS+"_"+self.faceS



app = Flask(__name__)

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
    Player_list[request.sid] = Player(name,faceS,hairS,hairC,skin,cloth)
    filePath = "/faceS"+faceS+"_hairS"+hairS+"_hairC"+hairC+"_hairS"+hairS+"_skin"+skin+"_cloth"+cloth+"/"
   ##return jsonify(faceS = request.get_json("faceS"),
   ##                 hairS = request.get_json("hairS"),
   ##                 hairC = request.get_json("hairC"),
   ##                 skin =  request.get_json("skin"),
   ##                 cloth = request.get_json("cloth"),)
    return  filePath


if __name__ == "__main__":
    app.run(debug=True)