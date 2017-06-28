# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from flask_login import login_required
from flaskapp.user.models import Room, db, Track
import requests
import time
import uuid
import random

client_id = ""
client_secret = ""
host_url = ""
blueprint = Blueprint('user', __name__, static_folder='../static')

@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')

@blueprint.route('/spauth/')
def spotify_auth():

    url = "https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}/callback&scope=user-read-private%20playlist-read-private%20playlist-modify-public%20playlist-modify-private&show_dialog=false".format(client_id, host_url)

    return redirect(url)

@blueprint.route('/callback', methods=['GET', 'POST'])
def callback_test():
    code = request.args.get("code", None)
    if code is None:
        return "invalid code"

    url = "https://accounts.spotify.com/api/token"
    payload = {"grant_type":"authorization_code", 
    "code":code, "redirect_uri":"{}/callback".format(host_url),
    "client_id":client_id, "client_secret":client_secret}


    req = requests.post(url, data=payload)

    reqjson = req.json()
    if not reqjson.get("access_token", None):
        return "sesh expired"
    gen_id = str(uuid.uuid4())
    another_req = requests.get("https://api.spotify.com/v1/me", headers={"Authorization":"Bearer {}".format(reqjson.get("access_token", None))}).json()
    room = Room.create(uuid_id=gen_id, token=reqjson.get("access_token", "None"), token_expiry=int(time.time()) + reqjson["expires_in"], password=generate_name(), username=another_req["id"], name="test")
    
    session["uuid_id"] = gen_id


    





    #session['room_host'] = 

    #print(req.content)
    return redirect(url_for('user.create_room'))

@blueprint.route("/createroom/", methods=['GET', 'POST'])
def create_room():
    if 'uuid_id' in session:
        uuid_id = session["uuid_id"]
        isAuth = True
    else:
        return "Not logged in"

    room_info = Room.query.filter_by(uuid_id=uuid_id).first()

    if not room_info:
        return "Room not found"

    url = "https://api.spotify.com/v1/users/{}/playlists".format(room_info.username)
    payload = {
        "name":"{}".format(room_info.password),
        "public":"false"
    }

    req = requests.post(url, headers={"Authorization":"Bearer {}".format(room_info.token), 
        "Content-Type":"application/json"}, json=payload).json()

    room_info.spotify_playlist_id = req["id"]
    room_info.save()

    flash("Playlist with the name {} has been created in your Spotify Account.".format(room_info.password))

    return redirect(url_for('user.room_view', f_id=uuid_id))
    #render_template("create_room.html", isAuth = isAuth, name = uuid_id)


def generate_name():
    animals = [
      "alligator",
      "ape",
      "badger",
      "bat",
      "bear",
      "bison",
      "boar",
      "buffalo",
      "bull",
      "camel",
      "canary",
      "cat",
      "chameleon",
      "cheetah",
      "chipmunk",
      "cow",
      "crocodile",
      "crow",
      "deer",
      "dingo",
      "dog",
      "donkey",
      "elephant",
      "fish",
      "fox",
      "frog",
      "gazelle",
      "giraffe",
      "goat",
      "gorilla",
      "hamster",
      "hedgehog",
      "hog",
      "horse",
      "jaguar",
      "kangaroo",
      "koala",
      "lamb",
      "lemur",
      "leopard",
      "lion",
      "lizard",
      "mandrill",
      "mink",
      "mongoose",
      "monkey",
      "mouse",
      "muskrat",
      "mustang",
      "ocelot",
      "panda",
      "panther",
      "parrot",
      "pig",
      "puma",
      "rabbit",
      "raccoon",
      "ram",
      "rat",
      "reptile",
      "seal",
      "sheep",
      "sloth",
      "snake",
      "squirrel",
      "tapir",
      "tiger",
      "toad",
      "turtle",
      "walrus",
      "weasel",
      "whale",
      "wildcat",
      "wolf",
      "yak",
      "zebra"
    ]

    rand = random.randint(1, 99)

    sr = random.choice(animals) + str(rand)

    # check if its unique
    if Room.query.filter_by(password=sr).first():
        return generate_name()
    else:
        return sr

@blueprint.route("/join", methods=['GET', 'POST'])
def join():

    if request.method == 'POST':
        code = request.form['room_code']
        room_info = Room.query.filter_by(password=code).first()
        if room_info:
            return redirect(url_for('user.room_view', f_id=room_info.uuid_id))
        else:
            flash("Room not found.")



    return redirect("/")

@blueprint.route("/room/<f_id>")
def room_view(f_id):
    room_info = Room.query.filter_by(uuid_id=f_id).first()

    if room_info:
      return render_template("room_view.html", room=room_info, title="{} @ roombox".format(room_info.password), time=int(time.time()))
    else:
      return "Room is not found. Please <a href='/'>click here</a> to go back to home page"

@blueprint.route("/room/<id>/search", methods=["GET"])
def room_search(id):
    room_info = Room.query.filter_by(uuid_id=id).first()
    if not room_info:
        return "Room is not found."

    f = request.args.get('q', '')
    if f != '':
        url = "https://api.spotify.com/v1/search?q={}&type=track".format(request.args.get("q"))
        search_results = requests.get(url, headers={"Authorization":"Bearer {}".format(room_info.token)}).json()["tracks"]["items"]
        return render_template("room_search.html", s=search_results)
    else:
        return render_template("room_search.html")

@blueprint.route("/room/<rid>/add/<uri>")
def add_song(rid, uri):
    room_info = Room.query.filter_by(uuid_id=rid).first()

    if not room_info:
        return "Room is not found."

    url = "https://api.spotify.com/v1/tracks/{}".format(uri)
    ree = requests.get(url=url).json()

    artists = ree["artists"]
    artist = ""
    comma = False
    ar_lists = []
    for i in artists:
        ar_lists.append(i["name"])

    artist = ", ".join(ar_lists)
    
    url = "https://api.spotify.com/v1/users/{}/playlists/{}/tracks?uris={}".format(room_info.username, room_info.spotify_playlist_id, ree["uri"])


    req = requests.post(url, headers={"Authorization":"Bearer {}".format(room_info.token)})
    track = Track(uri=uri, artist=artist, name=ree["name"])

    room_info.tracks.append(track)
    room_info.save()


    flash("Song successfully added.")
    return redirect(url_for('user.room_view', f_id=rid))



