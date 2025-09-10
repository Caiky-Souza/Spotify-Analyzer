
from config import *
from flask import *
from functools import wraps
import requests


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("access_token") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_user():
    user = requests.get(api_url + "/v1/me", headers={
        "Authorization":"Bearer " + session["access_token"]
    })

    return user.json()

def get_top_artists():
    artists = requests.get(api_url + "/v1/me/top/artists?limit=20&time_range=medium_term", headers={
        "Authorization":"Bearer " + session["access_token"]
    }).json()

    return artists

def get_top_tracks():
    tracks = requests.get(api_url + "/v1/me/top/tracks?limit=50&time_range=medium_term", headers={
        "Authorization":"Bearer " + session["access_token"]
    }).json()

    return tracks

def get_genres():
    top_tracks = get_top_tracks()["items"]
    total_genres = {}

    for track in top_tracks:
        for artist in track["artists"]:
            artist_href = artist["href"]

            artist = requests.get(f"{artist_href}", headers={"Authorization":"Bearer " + session["access_token"]}).json()
            for genre in artist["genres"]:
                try: 
                    total_genres[genre]
                except KeyError:
                    total_genres[genre] = 1
                else:
                    total_genres[genre] += 1
    
    return total_genres