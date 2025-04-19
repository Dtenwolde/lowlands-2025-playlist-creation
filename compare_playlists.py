import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Authenticate using Client Credentials Flow (no user login)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# === Helper: Get all track URIs from a playlist ===
def get_playlist_tracks(playlist_id):
    tracks = []
    offset = 0

    while True:
        response = sp.playlist_items(
            playlist_id,
            offset=offset,
            fields="items.track.id,items.track.name,items.track.artists.name,total",
            additional_types=['track']
        )

        if not response["items"]:
            break

        for item in response["items"]:
            track = item["track"]
            if track:  # skip local or unavailable tracks
                track_id = track["id"]
                name = track["name"]
                artist = track["artists"][0]["name"]
                tracks.append({
                    "id": track_id,
                    "name": name,
                    "artist": artist
                })

        offset += len(response["items"])

    return tracks

# === Main: Compare Playlists ===
def compare_playlists(playlist_a_id, playlist_b_id):
    print("📥 Fetching tracks from Playlist A...")
    a_tracks = get_playlist_tracks(playlist_a_id)
    print(f"✅ Playlist A has {len(a_tracks)} tracks")

    print("📥 Fetching tracks from Playlist B...")
    b_tracks = get_playlist_tracks(playlist_b_id)
    print(f"✅ Playlist B has {len(b_tracks)} tracks")

    # Convert to dictionaries for fast comparison
    a_dict = {t["id"]: t for t in a_tracks if t["id"]}
    b_dict = {t["id"]: t for t in b_tracks if t["id"]}

    only_in_a = [t for tid, t in a_dict.items() if tid not in b_dict]
    only_in_b = [t for tid, t in b_dict.items() if tid not in a_dict]

    print(f"\n🎧 Tracks only in Playlist A ({len(only_in_a)}):")
    for t in only_in_a:
        print(f"- {t['name']} by {t['artist']}")

    print(f"\n🎧 Tracks only in Playlist B ({len(only_in_b)}):")
    for t in only_in_b:
        print(f"- {t['name']} by {t['artist']}")

# === Run the comparison ===
if __name__ == "__main__":
    # Replace these with your actual playlist IDs (the long string after "playlist/")
    PLAYLIST_A_ID = "https://open.spotify.com/playlist/68l8JObS0eACSrLyutSw90?si=dc9aa93dcf4246eb"
    PLAYLIST_B_ID = "https://open.spotify.com/playlist/78mksc3X0mjnDfHGmK9yqb?si=4bd568de2a2f42a1"

    compare_playlists(PLAYLIST_A_ID, PLAYLIST_B_ID)