from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv('.env')  # loads the environment file

CLIENT_ID = os.getenv("CLIENT_ID")  # spotify client id
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # spotify client secret

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                                    redirect_uri="http://example.com",
                                                    client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET,
                                                    show_dialog=True,
                                                    cache_path="token.txt"))  # creates a Spotipy object

user_id = spotify.current_user()["id"]  # takes the current user id

date = input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD: ")  # takes date input
year = date.split("-")[0]  # takes the year from the input of the user

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")  # get request to the billboard website

billboard_data = response.text  # gets the text of the response

# chart_elements = []  # list destined to hold html tags
song_titles = []  # list destined to hold song titles
queries = []  # list destined to hold queries for songs in Spotify
song_uris = []  # list destined to hold uris of the songs

soup = BeautifulSoup(billboard_data, "html.parser")  # creates a BeautifulSoup project

chart_elements = soup.select(".chart-element__information__song")  # selects elements of class
# chart-element__information__song and returns a list of html tags with that class

for element in chart_elements:
    song_titles.append((element.getText()))  # gets the text inside the html tags and appends it into song_titles

# song_titles is now a list of strings, where each string is the title of a song. Those titles were scrapped from
# the Billboard website thanks to BeautifulSoup

# print(song_titles)

for song_title in song_titles:
    queries.append(f"track:{song_title} year:{year}")  # using the song_title, we make a new string for Spotify queries

print(queries)

for query in queries:
    result = spotify.search(q=query, type="track")  # gets the result of the query from the Spotify API via Spotipy
    try:
        uri = result['tracks']['items'][0]['uri']  # taps into the result object in order to find the URI of a song
        print(uri)
        song_uris.append(uri)  # appends the URI found inside the list song_uris
    except IndexError:
        print(f"{query} doesn't exist in Spotify. Skipped.")
        continue

playlist = spotify.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False,
                                        description=f"Playlist of the top hits in {year} ")  # creates a playlist

spotify.playlist_add_items(playlist_id=playlist['id'], items=song_uris)  # add tracks to the playlist
