import os
import json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="playlist-read-private"
    )
)

PLAYLIST_ID = "37i9dQZF1DXcBWIGoYBM5M"  

results = sp.playlist_items(PLAYLIST_ID, limit=100)

os.makedirs("data/raw", exist_ok=True)

with open("data/raw/playlist_items.json", "w") as f:
    json.dump(results, f, indent=2)

print("Playlist data saved to data/raw/playlist_items.json")
