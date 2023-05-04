from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("What date would you like to travel to? Type the date in the format YYYY-MM-DD: ")

# scrape the Billboard 100 website for the inputted date
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
response.raise_for_status()
web_text = response.text

# create
soup = BeautifulSoup(web_text, "html.parser")
print(soup)
songs = soup.find_all("div", class_="o-chart-results-list-row-container")
print(songs[0])
song_list = []
artists = []


song_list = soup.select("li ul li h3")
song_names = [song.get_text(strip=True) for song in song_list]
print(song_names)

# Connect to spotify
client_id = "f292f62dd5f44b1298e6754c80be271a"
client_secret = "b7d2352e3ef943af9e8ca5b07f638f18"
SPOTIPY_REDIRECT_URI = "http://example.com/"
spotipy_scope = "playlist-modify-public"
spotify_username = "116238293"

token = SpotifyOAuth(client_id=client_id,
                     client_secret=client_secret,
                     redirect_uri=SPOTIPY_REDIRECT_URI,
                     state=None,
                     scope=spotipy_scope,
                     username=spotify_username)

spotify_object = spotipy.Spotify(auth_manager=token)

# create playlist
spotify_object.user_playlist_create(user=spotify_username,
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

pre_playlist = spotify_object.user_playlists(user=spotify_username)

playlist = pre_playlist["items"][0]["id"]

# add songs
spotify_object.playlist_add_items(playlist_id=playlist, items=song_uris)
