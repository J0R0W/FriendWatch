import os
import random
import sched
import string
import atexit
import time
from threading import Timer as threadT

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, json, session, abort, redirect, url_for

from utility import RepeatedTimer

app = Flask(__name__)
app.secret_key = "iguzuzcsd89sd80f9z08whwucf03q2cd08hcwkjkjsdqq"
videoPath = "static/video"
adminTime = 4
# Dictonary of All Avaible Rooms
Rooms = {}


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
        #abort(403)


@app.route('/create', methods=['POST'])
def createwatch():
    if (request.method == "POST"):
        vid = request.form.get("video")
        vid = secure_filename(vid)
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        v = Raum(code, "pause", vid)
        Rooms[code] = v
        #Store a link to a Video in a Txt File
        if(vid.endswith('txt')):
            path = os.getcwd()
            path = os.path.join(path, "static")
            path = os.path.join(path, "video")
            path = os.path.join(path, vid)
            f = open(path, "r")
            videolocation = f.read()
            Rooms[code].video = videolocation
            Rooms[code].type = "txt"
        return redirect("/watch-" + code, code=302)
        #return render_template("watch.html", code=code, video=vid)
    return


@app.route('/layout')
def lay():
    return 'Hello World!'

@app.route('/watch', methods=['POST'])
def fnwatch():
    if (request.method == "POST"):
        code = request.form.get("codeIn")
        return redirect("/watch-" + code, code=302)

# Update Status if Play or Pause pressed
@app.route('/videoStatus', methods=['POST'])
def videostatus():
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
        r.time = float(videotime)
    elif (videoEvent == "pause"):
        r.status = videoEvent
    return json.dumps({'status': 'OK', 'user': "Test"});


@app.route('/updateVideo', methods=['POST'])
def updatetime():
    videotime = request.form['time']
    videoid = request.form['id']
    try:
        r = Rooms[videoid]
        print(r.status)

        # if abs(r.lastPlay + float(videotime) - time.time()) > 1:
        if abs(r.time - float(videotime)) > 1:
            return json.dumps({'time': r.time, "updated": True, 'status': r.status})
        return json.dumps({"noupdate": False, 'status': r.status})
    except:
        return "Bad Room-Code"



@app.route("/startwatch")
def startwatch():
    if session.get('user') == "admin":

        path = os.getcwd()
        path = os.path.join(path, "static")
        path = os.path.join(path, "video")
        # path = videoPath
        list_of_files = {}

        for filename in os.listdir(path):
            list_of_files[filename] = "/static/video" + filename
        return render_template("startwatch.html", videos=list_of_files)
    else:
        abort(403)

def calculateTime():
    for key, value in Rooms.items():
        if value.status == "play":
            value.time += 0.25
            #print("update Raum " + key + " " + str(value.time))

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
#timer = threadT(0.1, calculateTime).start()
ti = RepeatedTimer(0.25, calculateTime)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1337)
