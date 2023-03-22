import requests
import bs4
#import spotify
import sys
import threading
import numpy as np
import scrapebands
import collections

"""
Contact: Brendan Griffen brendan.f.griffen@gmail.com @brendangriffen

Code will scrape bands playing in next few months in Boston area.

Requirements:

spotipy:        https://spotipy.readthedocs.io/en/2.22.1/?highlight=playlist#
developer key:  https://developer.spotify.com/dashboard/applications

Enjoy the tunes!

"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
                                               scope=scope))

# get bands in the coming 3 months weeks
dfbands = scrapebands.get_bands(num_weeks=12)
all_bands = list(dfbands['band_name'].str.title())

print("Here is the dataframe of bands to be added...")
print(dfbands)

print("Clearing current tracks...")
current_tracks = sp.user_playlist(os.environ['SPOTIFY_USER_ID'], playlist_id=os.environ['SPOTIFY_CLIENT_PLAYLISTID'])['tracks']
remove_tracks = [item['track']['uri'] for item in current_tracks['items']]
if remove_tracks:
    sp.user_playlist_remove_all_occurrences_of_tracks(os.environ['SPOTIFY_USER_ID'],
                                                  playlist_id=os.environ['SPOTIFY_CLIENT_PLAYLISTID'],
                                                  tracks=remove_tracks)

for band in all_bands:
    results = sp.search(q='artist:' + band, type='artist')
    artist = results['artists']['items']

    # if there are artists proceed...
    if len(artist) > 0:
        lz_uri = artist[0]['uri']

    print("Adding",band)
    # just get top 2 tracks if available
    top_tracks = sp.artist_top_tracks(lz_uri)['tracks'][:2]
    add_tracks = [track['uri'] for track in top_tracks]
    # add those to playlist
    if len(add_tracks) == 0:
            print("> Skipping - no tracks!")
            continue

    sp.user_playlist_add_tracks(os.environ['SPOTIFY_USER_ID'], playlist_id=os.environ['SPOTIFY_CLIENT_PLAYLISTID'], tracks=add_tracks)

    # remove duplicates
    current_tracks = sp.user_playlist(os.environ['SPOTIFY_USER_ID'], playlist_id=os.environ['SPOTIFY_CLIENT_PLAYLISTID'])['tracks']
    track_list = [item['track']['uri'] for item in current_tracks['items']]
    duplicate_tracks = set([x for x in track_list if track_list.count(x) > 1])
    sp.user_playlist_remove_all_occurrences_of_tracks(os.environ['SPOTIFY_USER_ID'],
                                                      playlist_id=os.environ['SPOTIFY_CLIENT_PLAYLISTID'],
                                                      tracks=duplicate_tracks)

    # add them back singularly
    sp.user_playlist_add_tracks(os.environ['SPOTIFY_USER_ID'], playlist_id=os.environ['SPOTIFY_CLIENT_PLAYLISTID'], tracks=duplicate_tracks)
