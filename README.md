# 🎶 Lowlands 2025 Playlist Generator

This script automatically creates a Spotify playlist with songs from the **latest album of every artist performing at Lowlands 2025**.

Artist information is scraped from the [official Lowlands website](https://lowlands.nl/acts/), and the playlist is created using the [Spotify Web API](https://developer.spotify.com/documentation/web-api/).

<p align="center">
  <img src="https://lowlands.nl/media/images/LL25_facebook_HeaderEventPage-192.2e16d0ba.fill-1200x628.jpg" alt="Lowlands Logo" width="200"/>
</p>

---

## 🧠 What It Does

- Scrapes the full lineup from [https://lowlands.nl/acts/](https://lowlands.nl/acts/)
- Extracts Spotify artist links from artist pages
- Fetches each artist’s **most recently released full album**
- Adds all tracks from those albums to a new Spotify playlist in your account

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dtenwolde/lowlands2025-playlist.git
cd lowlands2025-playlist
```

### Install dependencies
```bash 
pip install -r requirements.txt
```

### Set up Spotify API credentials
Create a .env file in the root of the project and add your credentials:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8080/callback
SPOTIFY_USERNAME=your_spotify_username
```

### Run the script
```bash
python latest_albums.py
python most_listened_songs.py
```

### ✅ Requirements
* Python 3.7+
* Spotify Premium account (required to manage playlists through the API)

### 🛡 Security Notice
Your credentials are stored in a .env file which is excluded from version control using .gitignore. Never commit this file to a public repository.


Feel free to contribute or open issues!