#import libraries for spotify API, and pandas for data manipulation

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

#Create a client credentials object to store your keys
#NOTICE -- I did not include my actual keys here and you should keep yours confidential as well

client_credentials_manager = SpotifyClientCredentials(client_id = '<your client id>', client_secret = '<your secret id>')

#now that you have an object storing your keys, we can instantiate a spotipy object that has access to the methods we care about

sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)





#many methods rely on a uniform resource indicator (URI)
#It is a part of the URL link that serves as a unique id for any playlist, song, album, artist, etc.

my_playlist_link = 'https://open.spotify.com/playlist/1Vl23QvujvM5kROoqjF1fC?si=1c68f80304cf4bc0'

#extract just the URI, the string between the last '/' and the '?'

my_playlist_URI = my_playlist_link.split("/")[-1].split("?")[0]

#pull the album, song, and artist level data for every song on my playlist

tracks_in_my_playlist_info = sp.playlist_tracks(my_playlist_URI)





#create lists to store these fields for each of the playlist songs

song_uri = []
song_name = []
artist = []
artist_main_genre = []
song_popularity = []


#loop through the 'items' list

for entry in tracks_in_my_playlist_info["items"]:

#extract the URI, splitting the link string 

song_uri.append(entry["track"]["uri"].split(":")[-1])
#append the song name

song_name.append(entry["track"]["name"])

#from the list of artists (potentially more than one), select only the first one and append their name

artist.append(entry["track"]["artists"][0]["name"])

#From the artist's URI, we can use the .artist method to get the main artist's main genre as a proxy for the song. 
#However, some artist profiles do not have genres, so we must add an exception rule if the 'genres' list returns empty

try:
    artist_main_genre.append(sp.artist(entry["track"]["artists"][0]["uri"])["genres"][0])
except IndexError:
    artist_main_genre.append("unknown")

#append the song's popularity

song_popularity.append(entry["track"]["popularity"])





#create a dataframe with these lists as values and their names as column names

basic_song_data = pd.DataFrame({'song_uri': song_uri,
'song_name': song_name,
'artist': artist,
'genre' : artist_main_genre,
'popularity': song_popularity})





#Feed our song URIs to the audio_features method to pull various musical metrics

detailed_song_features = sp.audio_features(basic_song_data['song_uri'])

#if you were to print detailed_song_features, you'd receive a list of dictionary entries. 
#Each dictionary represents one song, with metric names as keys and metric values as values. 
#Given that, we can convert the keys that each dictionary shares into columns and the sets of values as rows of a DataFrame using .from_dict()

detailed_song_features = pd.DataFrame.from_dict(detailed_song_features)





#merge the basic and detailed song dataframes on their columns that contain URIs of the songs

all_song_data_for_my_playlist = pd.merge(left = basic_song_data, 
                                         right = detailed_song_features, 
                                         left_on = "song_uri", 
                                         right_on= "id")

#We probably do not need all of these columns. In the next step of this project, I plan to use danceability and valence
#duration may also be interesting to visualize, so we can select those out of the musical metrics.
simple_song_data_for_my_playlist = all_song_data_for_my_playlist[["song_name", 
                                                                  "artist", 
                                                                  "genre", 
                                                                  "popularity", 
                                                                  "danceability", 
                                                                  "valence", 
                                                                  "duration_ms"]]