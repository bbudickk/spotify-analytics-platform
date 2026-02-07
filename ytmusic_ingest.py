from ytmusicapi import YTMusic
import json
import os

ytmusic = YTMusic()

PLAYLIST_ID = "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj"  # Example: "Top 100 Global"

playlist = ytmusic.get_playlist(PLAYLIST_ID, limit=50) 

os.makedirs("data/raw", exist_ok=True)

with open("data/raw/yt_playlist.json", "w", encoding="utf-8") as f:
    json.dump(playlist, f, indent=2, ensure_ascii=False)

print("YouTube Music playlist saved to data/raw/yt_playlist.json")
