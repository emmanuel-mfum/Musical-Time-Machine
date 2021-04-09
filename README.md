# Musical-Time-Machine
Python app that allows the user to create private Spotify playlists via the libraries Beautiful Soup and Spotipy.

Songs can make us recall memories, good or bad, especially when these songs date from a while back. This program will help the users
make his own private playlists on Spotify based on the top songs of the Billboard 100 of a date given by the user.

First of all, we need to create a Spotify account for developers (https://developer.spotify.com/).
By making an account, we will get a client id and a client secret. These two credentials will be useful later when using Spotipy.

Then we need to scrape the Billboard 100 website for the title of songs for a particular date.

The date is taken from an input by the user (in the correct format, YYYY-MM-DD) and inserted in the URL of the GET request to the Billboard 100 website.
Once we get the response from the request, we extract the text of the response and pass it into the BeautifulSoup constructor in order to make a 
BeautifulSoup object.

Within the html text parsed by BeautifulSoup, we look for items with the class "chart-element__information__song" and each item is stored into a list.
A second list is then made where we extract the text (the song title) of the items of the first list and store them inside it.

These song titles collected are then used to make a series of string of the form "track:{song_title} year:{year}". These strings are going to be used for our queries
for the Spotify API via Spotipy.

We also need to authenticate ourselves with Spotipy, using our credentials. To know, we consulted the documentation of Spotipy (https://spotipy.readthedocs.io/en/2.17.1/).
We notably needed to pass our client id and secret into the SpotifyOAuth() constructor, pass appropriate properties and ajust settings in our Spotify dashboard (create a Spotify app on our dashboard and setting a redirect URL).

The next step is to search for our songs in Spotify using the Spotipy library. To do that we pass our query strings inside the search() method of Spotipy and specify the
type parameter as "track". We get a result from our query and we try to tap into that result for the song's URI. If no error is thrown, we store the URI we just found into
a list, otherwise we continue this process for all the song titles.

Once we have found all the URIs for the songs, we use the "user_playlist_create()" method from Spotipy in order to create a private playlist and by providing the necessary 
arguments for the parameters (thsi can be found on the Github page of Spotipy). After the creation of playlist (which returns a playlist object), we add the songs into our playlist by using the Spotipy method called" playlist_add_items()" and passing the id of our playlist as well as our list of song's URIs (we pass the list itself, in its 
entirety).

This project of course requires having a Spotify account for developers and proper credentials as well as having a Python environment installed on one's computer.





