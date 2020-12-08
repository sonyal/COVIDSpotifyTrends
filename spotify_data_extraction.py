import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
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




for filename in os.listdir(os.getcwd()+'/top200_data'):    
    start_date = filename[19:29]
    end_date = filename[31:41]
    data = pd.read_csv('data.csv')
    top = pd.read_csv(os.getcwd() + '/top200_data/'+filename)
    temp = top.URL
        
    tracks = []

    for url in temp:
        track = getTrackFeatures(url[31:])
        tracks.append(track)

    temp = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
        
    temp['start_date'] = start_date
    temp['end_date'] = end_date
    temp.to_csv((os.getcwd() + "/top200_data/temp.csv"), sep = ',')
    temp = pd.read_csv(os.getcwd() + '/top200_data/temp.csv')
    temp = temp.drop(temp)
    os.remove(os.getcwd() + '/top200_data/temp.csv')

    print(temp, data)

    temp = data.append(temp)
    
    temp.to_csv("data.csv", sep = ',')
