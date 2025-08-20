import argparse
import yaml
from pathlib import Path
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date
import os

spotify_client_id = os.getenv("spotifyclientid")
spotify_client_secret = os.getenv("spotifyclients")

sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret
))

def fetch_playlist_tracks(playlist_url):
    playlist = sp.playlist(playlist_url)
    items = playlist["tracks"]["items"]
    tracks = []
    for item in items:
        track = item["track"]
        if not track:
            continue
        tracks.append({
            "title": track["name"],
            "artist": ", ".join([a["name"] for a in track["artists"]]),
            "link": track["external_urls"]["spotify"],
            "platform": "spotify",
            "genre": "",
            "mood": "",
            "year": int(track["album"]["release_date"][:4]) if track["album"]["release_date"] else "",
            "date_added": str(date.today()),
            "notes": ""
        })
    return tracks

def load_library(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []

def save_library(path, tracks):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(tracks, f, allow_unicode=True, sort_keys=False)

def deduplicate(existing, new):
    existing_links = {t["link"] for t in existing}
    return existing + [t for t in new if t["link"] not in existing_links]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    path = Path("music/data/libraryspotify.yaml")
    existing = load_library(path)
    new = fetch_playlist_tracks(args.url)
    updated = deduplicate(existing, new)
    added_count = len(updated) - len(existing)
    save_library(path, updated)
    print(f"{added_count} new track(s) added to music/data/libraryspotify.yaml")

if __name__ == "__main__":
    main()

