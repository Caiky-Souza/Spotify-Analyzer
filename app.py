import requests, os

from helpers import *
from config import client_id, redirect_ui, base64_string, scopes_string, header, api_url
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)


app.secret_key = os.urandom(12) 


@app.route("/get",methods=["POST"])
@login_required
def get_data():
    if request.method == "POST":
        action = request.get_json()
        action = action.get("action")
        print(action)
        if action == "get_genres":
            genres = get_genres()
            return genres
            

@app.route("/")
@login_required
def home():
    user = get_user()
    username = user["display_name"]
    top_tracks = get_top_tracks()["items"]
    top_artists = get_top_artists()["items"]
    
    return render_template("index.html", user=username, tracks=top_tracks, artists=top_artists)

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        if request.form.get("submit-login"):
            return redirect(f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_ui}&scope={scopes_string}")

@app.route("/logout")
def logout():
    try:
        session.pop("access_token")
    except: 
        pass
    
    return redirect("https://accounts.spotify.com/logout")

@app.route("/callback", methods = ["GET","POST"])
def callback():
    error = request.args.get("error")

    if error:
        return render_template("error.html", error=error)
    
    data = {
    "grant_type":"authorization_code",
    "code":request.args.get("code"),
    "redirect_uri":redirect_ui
}
    
    response = requests.post("https://accounts.spotify.com/api/token",headers=header,data=data)

    try:
        session['access_token'] = response.json().get("access_token")
    except:
        print("Ops, tivemos um problema")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)