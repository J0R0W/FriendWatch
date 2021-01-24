import os
import random
import string
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, json, session, abort, redirect, url_for
from utility import RepeatedTimer

app = Flask(__name__)
app.secret_key = "iguzuzcsd89sd80f9z08whwucf03q2cd08hcwkjkjsdqq"
videoPath = "static/video"
adminTime = 4
# Dictonary of All Avaible Rooms
Rooms = {}


# Class to manage Rooms
class Raum:
    def __init__(self, raumCode, status, video):
        self.raumCode = raumCode
        self.status = status
        self.video = video
        self.time = float(0)
        self.lastPlay = 0
        self.type = "video"


@app.route('/')
def hello_world():
    return render_template("enterCode.html")


@app.errorhandler(404)
def err404(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def err403(e):
    return render_template("403.html"), 403


@app.route('/watch-<string:code>')
def watch(code):
    try:
        return render_template("watch.html", code=code, video=Rooms[code].video, type=Rooms[code].type)
    except:
        return "Falscher Code"
        # abort(403)


@app.route('/create', methods=['POST'])
def createwatch():
    if (request.method == "POST"):
        vid = request.form.get("video")
        vid = secure_filename(vid)
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        v = Raum(code, "pause", vid)
        Rooms[code] = v
        # Store a link to a Video in a Txt File
        if vid.endswith('txt'):
            # get Path to Video Folder
            path = os.getcwd()
            path = os.path.join(path, "static")
            path = os.path.join(path, "video")
            path = os.path.join(path, vid)
            f = open(path, "r")
            # Read the Link to a video
            videolocation = f.read()
            Rooms[code].video = videolocation
            Rooms[code].type = "txt"
        return redirect("/watch-" + code, code=302)
    return


@app.route('/watch', methods=['POST'])
def joinwatch():
    if (request.method == "POST"):
        code = request.form.get("codeIn")
        return redirect("/watch-" + code, code=302)


# Update Status if Play or Pause pressed or if the Video Seeked
@app.route('/videoStatus', methods=['POST'])
def videostatus():
    # Get Params from POST request
    videoEvent = request.form['event']
    videotime = request.form['time']
    videoid = request.form['id']

    # Update the Status in the current Room
    r = Rooms[videoid]

    # If Video Already playing send current Play Time, else set current Position to Global position
    if videoEvent == 'play':
        if r.status == 'play':
            return json.dumps({'time': r.time, "updated": True, 'status': r.status})
        else:
            r.status = videoEvent
    if videoEvent == 'seeked':
        # update the Time for the Video
        r.time = float(videotime)
    elif videoEvent == "pause":
        r.status = videoEvent
    return json.dumps({'status': 'OK', 'user': "Test"});


# Method for request to read Video state and update client
@app.route('/updateVideo', methods=['POST'])
def updatetime():
    videotime = request.form['time']
    videoid = request.form['id']
    try:
        r = Rooms[videoid]

        # if abs(r.lastPlay + float(videotime) - time.time()) > 1:
        if abs(r.time - float(videotime)) > 1:
            return json.dumps({'time': r.time, "updated": True, 'status': r.status})
        return json.dumps({"noupdate": False, 'status': r.status})
    except:
        # The Room Code was not found
        return "Bad Room-Code"


@app.route("/startwatch")
def startwatch():
    if session.get('user') == "admin":
        # Get Path to Video Folder
        path = os.getcwd()
        path = os.path.join(path, "static")
        path = os.path.join(path, "video")
        list_of_files = {}
        #Put every File in Video Folder in the list
        for filename in os.listdir(path):
            list_of_files[filename] = "/static/video" + filename
        #return the Template with the List, of all files in the Video folder
        return render_template("startwatch.html", videos=list_of_files)
    else:
        abort(403)


# This Method is called every 0.25 Seconds to Update the Time for each active Room.
# The server calculates the current time depending on client events.
def calculateTime():
    for key, value in Rooms.items():
        if value.status == "play":
            value.time += 0.25


# Simple Login Method. Only One Username Exist.
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        passw = request.form.get("password")
        if user == "admin" and passw == "hugo":
            session["user"] = "admin"
        return redirect("/startwatch")
    else:
        return render_template("login.html")


# The Timer which calls the calculateTimeMethod
ti = RepeatedTimer(0.25, calculateTime)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1337)
