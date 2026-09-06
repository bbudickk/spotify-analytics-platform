import time
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv
import os
import json

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
client_uri = os.getenv("SPOTIFY_REDIRECT_URI")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id, 
    client_secret=client_secret,
    redirect_uri=client_uri,
    scope="user-library-read"))

def load_favorite_tracks(rate_limit: int):
    track_dict = []
    try:
        results = sp.current_user_saved_tracks(limit=rate_limit)
    except SpotifyException as e:
        results = None
        print(f"That happend: {e}")

    track_count = 1
    while results:
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(track_count + idx, track['artists'][0]['name'], " – ", track['name'])
            track_dict.append(dict(
                track_id = track_count + idx,
                artist_name = track['artists'][0]['name'], 
                track_name = track['name'],
                release_date = track['album']['release_date'],
                track_uri=track['uri'],
            ))

        if results['next']:
            results = sp.next(results)
            track_count += idx + 1
            time.sleep(0.5)
        else:
            results = None
            with open('data/favorite_tracks.json', 'w', encoding="utf-8") as file:
                    json.dump(track_dict, file, ensure_ascii=False, indent=4)
                    print("Tracks was sucessfully write!")

load_favorite_tracks(20)

    