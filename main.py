from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

date = input("What date would you like to travel to? Type the date in the format YYYY-MM-DD: ")

# scrape the Billboard 100 website for the inputted date
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
response.raise_for_status()
web_text = response.text

# Connect to spotify
SPOTIPY_REDIRECT_URI = "http://example.com/"
spotipy_scope = "playlist-modify-public"

token = SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     redirect_uri=SPOTIPY_REDIRECT_URI,
                     state=None,
                     scope=spotipy_scope,
                     username=os.getenv('SPOTIFY_USERNAME'))

spotify_object = spotipy.Spotify(auth_manager=token)

# create playlist
spotify_object.user_playlist_create(user=os.getenv('SPOTIFY_USERNAME'),
                                    name=f"A blast from the past: {date}",
                                    public=True,
                                    description=f"A collection of the 100 most popular song on the date {date}")

# Make list of song names
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_website = response.text
soup = BeautifulSoup(billboard_website, "html.parser")
all_songs = soup.find_all(name="div", class_="o-chart-results-list-row-container")
songs = [song.find("h3").getText().strip() for song in all_songs]

# find songs uri's
song_uris = []
for song in songs:
    try:
        result = spotify_object.search(q=song)
        song_uris.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"Song not found: {song}")

# load playlists
all_playlists = spotify_object.user_playlists(user=os.getenv('SPOTIFY_USERNAME'))
# [0]["id"] used as the likelihood of the user creating another playlist in the time
# it takes to run the program is very low
playlist_id = all_playlists["items"][0]["id"]

# add songs to playlist
spotify_object.playlist_add_items(playlist_id=playlist_id, items=song_uris)
