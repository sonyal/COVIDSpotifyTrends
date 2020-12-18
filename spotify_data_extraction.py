import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np


try:
    client_id = open('client_id.txt').read()
    client_secret = open('client_secret.txt').read()
except:
    print("error")

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def getTrackFeatures(id):
  meta = sp.track(id)
  features = sp.audio_features(id)

  # meta
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']

  # features
  acousticness = features[0]['acousticness']
  danceability = features[0]['danceability']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']

  track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
  return track



ct = 0
tracks = []


for filename in os.listdir(os.getcwd()+'/top200_data'):    
    try:
        start_date = filename[19:29]
        end_date = filename[31:41]
        top = pd.read_csv(os.getcwd() + '/top200_data/'+filename)
        temp = top.URL[:20]
        

        for url in temp:
            track = getTrackFeatures(url[31:])
            track.append(start_date)
            track.append(end_date)
            tracks.append(track)
        

        ct += 1
    except:
        print('Unable to extract from '+ filename)

print(str(ct) + " files completed")

try:
    temp = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature','start_date','end_date'])
    temp.to_csv("data.csv", sep = ',', index=False)
except:
    print("Unable to save song data to csv")
