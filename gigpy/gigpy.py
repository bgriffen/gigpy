import requests
import bs4
import spotipy
import os
import collections
from spotipy.oauth2 import SpotifyOAuth
import yaml
import logging

import tools
import helper

"""
Contact: Brendan Griffen @brendangriffen

Code will scrape bands playing in next few months in various cities.

Requirements:

spotipy:        https://spotipy.readthedocs.io/en/2.22.1/?highlight=playlist#
developer key:  https://developer.spotify.com/dashboard/applications

Enjoy the tunes!

"""

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
                                               scope=scope))


logging.basicConfig(level=logging.INFO)


def generate_playlist_for_city(city):
    """
    Generate a Spotify playlist for a given city

    :param city: A String representing the city name
    :return: None
    """
    try:
        playlist_id = helper.city_to_playlist[city]
    except KeyError:
        logging.error(f"Sorry, there is no playlist for {city}.")
        return

    logging.info(f"RUNNING: {city}")
    logging.info("Getting upcoming bands..")
    dfbands = tools.get_bands(city=city, num_weeks=12, window_size=3)
    all_bands = list(dfbands['band_name'].str.title())
    logging.info("Here is the dataframe of bands to be added...")
    logging.info(dfbands)

    logging.info("Clearing current tracks...")
    remove_and_add_tracks(playlist_id, all_bands)
    logging.info("Adding bands to playlists...")
    for band in all_bands:
        add_playlists_for_band(band, playlist_id)

def remove_and_add_tracks(playlist_id, all_bands):
    """
    Removes existing tracks and adds new ones to the playlist

    :param playlist_id: A string representing the Spotify playlist ID
    :param all_bands: A list of band names
    :return: None
    """
    current_tracks = sp.user_playlist(os.environ['SPOTIFY_USER_ID'], playlist_id=playlist_id)['tracks']
    remove_tracks = [item['track']['uri'] for item in current_tracks['items']]
    while remove_tracks:
        logging.info(f"Removing {len(remove_tracks)} tracks...")
        current_tracks = sp.user_playlist(os.environ['SPOTIFY_USER_ID'], playlist_id=playlist_id)['tracks']
        remove_tracks = [item['track']['uri'] for item in current_tracks['items']]
        if remove_tracks:
            print(remove_tracks)
            sp.user_playlist_remove_all_occurrences_of_tracks(os.environ['SPOTIFY_USER_ID'],
                                                          playlist_id=playlist_id,
                                                          tracks=remove_tracks)

def add_playlists_for_band(band, playlist_id):
    """
    Finds an artist's songs and adds them to a Spotify playlist

    :param band: A string representing the band name
    :param playlist_id: A string representing the Spotify playlist ID
    :return: None
    """
    results = sp.search(q='artist:' + band, type='artist')
    artist = results['artists']['items']

    if not artist:
        logging.error("> Skipping - band not found!")
        return

    lz_uri = artist[0]['uri']
    top_tracks = sp.artist_top_tracks(lz_uri)['tracks'][:2]
    add_tracks = [track['uri'] for track in top_tracks]

    if not add_tracks:
        logging.error("> Skipping - no tracks for the band!")
        return
    else:
        logging.info(f"Adding tracks for {band}")
        sp.user_playlist_add_tracks(os.environ['SPOTIFY_USER_ID'], playlist_id=playlist_id, tracks=add_tracks)

def cleanup(playlist_id):
    """
    Function to clean up the playlist by removing duplicate tracks and re-adding them back singly

    :param playlist_id: String, the Spotify Playlist ID
    :return: None
    """
    current_tracks = sp.user_playlist(os.environ['SPOTIFY_USER_ID'], playlist_id=playlist_id)['tracks']
    track_list = [item['track']['uri'] for item in current_tracks['items']]
    duplicate_tracks = [x for x in track_list if track_list.count(x) > 1]

    if duplicate_tracks:
        sp.user_playlist_remove_all_occurrences_of_tracks(os.environ['SPOTIFY_USER_ID'],
                                                      playlist_id=playlist_id,
                                                      tracks=duplicate_tracks)
        sp.user_playlist_add_tracks(os.environ['SPOTIFY_USER_ID'], playlist_id=playlist_id, tracks=duplicate_tracks)

if __name__ == "__main__":
    #generate_playlist_for_city("Brisbane")
    #generate_playlist_for_city("Melbourne")
    #generate_playlist_for_city("Sydney")
    generate_playlist_for_city("Adelaide")
    #cleanup(playlist_id)
