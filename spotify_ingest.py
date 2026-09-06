""" Import system library to writing json"""
import os
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
client_uri = os.getenv("SPOTIFY_REDIRECT_URI")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id, 
    client_secret=client_secret,
    redirect_uri=client_uri,
    scope="user-library-read"))


def extract_favorite_tracks(page_size: int):
    """
        Extract favorites tracks from user library. 
        Parametrs: 
        - page_size - get 1 to 20 tracks per query.
        
        Return:
        - track_list - full tracklist without any formatting.
    """
    try:
        extracted_tracklist = sp.current_user_saved_tracks(limit=page_size)
    except SpotifyException as e:
        extracted_tracklist = None
        print(f"That happend: {e}")
    track_list = []

    while extracted_tracklist:
        for item in extracted_tracklist['items']:
            track = item['track']
            track_list.append(track)
        if extracted_tracklist['next']:
            extracted_tracklist = sp.next(extracted_tracklist)
        else:
            extracted_tracklist = None

    return track_list


def transform_favorite_tracks(track_list):
    """
        Transform tracklist to suit requirements. 
        Parametrs: 
        - track_list - list without any transformations.
        
        Return:
        - formated_tracklist - only neseccary data about favorite tracks.
    """
    formated_tracklist = []

    for track in track_list:
        formated_tracklist.append(
            {
                "artist_name": track['artists'][0]['name'], 
                "track_name":  track['name'],
                "release_date": track['album']['release_date'],
                "track_uri": track['uri']
            }
        )

    return formated_tracklist


def load_favorite_tracks(path: str, formated_tracklist: list):
    """
        Load json tracklist into file. 
        Parametrs: 
        - path - file path.
        - json_tracklist - complete tracklist in json format.
    """
    if formated_tracklist:
        with open(path, 'w', encoding="utf-8") as file:
            json.dump(formated_tracklist, file, ensure_ascii=False, indent=4)
            print("Tracks was sucessfully write!")
    else:
        print("Tracklist is empty!")



final_track_list = extract_favorite_tracks(20)
final_formated_tracklist = transform_favorite_tracks(final_track_list)
load_favorite_tracks('data/favorite_tracks.json', final_formated_tracklist)
