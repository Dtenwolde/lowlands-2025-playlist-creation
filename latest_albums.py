import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import time

from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
USERNAME = os.getenv("SPOTIFY_USERNAME")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-modify-public",
    username=USERNAME
))

# ------------------- STEP 1: SCRAPE ARTISTS ------------------- #
def get_lowlands_artist_links_with_spotify():
    headers = {"User-Agent": "Mozilla/5.0"}
    LOWLANDS_URL = "https://lowlands.nl/acts/"
    response = requests.get(LOWLANDS_URL, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error fetching Lowlands website: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    artist_elements = soup.select("a.act-list-item__button")

    artists = []
    for element in artist_elements:
        href = element.get("href")
        name_element = element.select_one("h2")
        name = name_element.text.strip() if name_element else "Unknown"

        artist_url = f"https://lowlands.nl{href}" if href and href.startswith("/") else href
        artist_response = requests.get(artist_url, headers=headers)
        if artist_response.status_code != 200:
            print(f"⚠️ Could not fetch artist page for {name}")
            continue

        artist_soup = BeautifulSoup(artist_response.text, "html.parser")
        spotify_link_tag = artist_soup.select_one("li.act-detail__social-item a[href*='spotify.com']")
        spotify_url = spotify_link_tag["href"] if spotify_link_tag else None

        artists.append({
            "name": name,
            "lowlands_url": artist_url,
            "spotify_url": spotify_url
        })
        print(f"✅ Added {name}: {spotify_url or 'No Spotify link'}")

        time.sleep(0.5)  # Respectful delay between requests

    print(f"\n✅ Total artists found: {len(artists)}")
    return artists

# ------------------- STEP 2: HELPER FUNCTIONS ------------------- #
def extract_artist_id_from_url(url):
    match = re.search(r"spotify\.com/artist/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None

# ------------------- STEP 3: GET LATEST ALBUM TRACKS ------------------- #
def get_latest_album_tracks(artist_id):
    if not artist_id:
        return []

    try:
        albums = sp.artist_albums(artist_id, album_type="album", country="NL", limit=10)["items"]
        seen = set()
        unique_albums = [album for album in albums if album["name"].lower() not in seen and not seen.add(album["name"].lower())]

        if not unique_albums:
            print("❌ No albums found.")
            return []

        latest_album = unique_albums[0]
        album_id = latest_album["id"]
        print(f"📀 Latest album: {latest_album['name']}")

        tracks_data = sp.album_tracks(album_id)
        return [track["uri"] for track in tracks_data["items"]]

    except Exception as e:
        print(f"⚠️ Error fetching latest album: {e}")
        return []

# ------------------- STEP 4: CREATE PLAYLIST ------------------- #
def create_playlist():
    playlist = sp.user_playlist_create(
        user=USERNAME,
        name="Lowlands 2025 Latest Albums",
        public=True,
        description="Songs from the latest album of each Lowlands 2025 artist."
    )
    return playlist["id"]

# ------------------- STEP 5: ADD TRACKS ------------------- #
def add_songs_to_playlist(playlist_id, track_uris):
    batch_size = 100
    for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i + batch_size]
        sp.playlist_add_items(playlist_id, batch)
        print(f"✅ Added {len(batch)} tracks to playlist ({i + len(batch)}/{len(track_uris)})")
    print("🎶 All songs added successfully!")

# ------------------- MAIN ------------------- #
def main():
    artists = get_lowlands_artist_links_with_spotify()
    if not artists:
        print("No artists found. Exiting.")
        return

    all_tracks = []
    for artist in artists:
        name = artist["name"]
        spotify_url = artist.get("spotify_url")

        if spotify_url:
            artist_id = extract_artist_id_from_url(spotify_url)
            print(f"\n🎧 Fetching latest album for: {name}")
            tracks = get_latest_album_tracks(artist_id)
            all_tracks.extend(tracks)
        else:
            print(f"ℹ️ No Spotify link for {name}")

    if not all_tracks:
        print("No songs found. Exiting.")
        return

    playlist_id = create_playlist()
    add_songs_to_playlist(playlist_id, all_tracks)
    print("✅ Playlist created successfully!")

if __name__ == "__main__":
    main()