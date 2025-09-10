import base64
import os
import dotenv

dotenv.load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")


api_url = "https://api.spotify.com"
auth_string_bytes = f"{client_id}:{client_secret}".encode("utf-8")
base64_string = base64.b64encode(auth_string_bytes).decode('utf-8')

redirect_ui = "https://bug-free-pancake-rx4w64x9x5qhxw7g-5000.app.github.dev/callback"

scopes = ["playlist-read-private", 
    "playlist-modify-private", 
    "playlist-modify-public", 
    "user-read-playback-position",
    "user-top-read",
    "user-read-recently-played",
    "user-read-email",
    "user-read-private"]




scopes_string = ""

    

for scope in scopes:
    scopes_string += scope + " "

scopes_string.strip()
scopes_string = scopes_string.replace(" ", "%20")
print(scopes_string)
header = {
    "Authorization": "Basic " + base64_string,
    "content_type":"application/x-www-form-urlencoded"
}