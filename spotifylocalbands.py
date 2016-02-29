import requests
import bs4
import spotify
import sys
import threading
import numpy as np

"""
Contact: Brendan Griffen brendan.f.griffen@gmail.com @brendangriffen

Code will scrape bands playing in next few months in Boston area.

Requirements:

libspotify:     https://developer.spotify.com/technologies/libspotify/
pyspotify:      https://github.com/mopidy/pyspotify
developer key:  https://devaccount.spotify.com/my-account/keys/

Enjoy the tunes!

"""


logged_in_event = threading.Event()

def connection_state_listener(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in_event.set()
        session = spotify.Session()

session = spotify.Session()
session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED,connection_state_listener)
session.login('brendan.f.griffen@gmail.com','password')

while not logged_in_event.wait(0.1):
     session.process_events()

url_name = "http://www.boweryboston.com/see-all-shows/"

response = requests.get(url_name)
soup = bs4.BeautifulSoup(response.text)

# scrape the relevant information and put into a list
bands_split = [elm.a.text.split(",") for elm in soup.find_all('h1',class_='headliners summary')]

# don't forget the support acts!
supports = [elm.a.text for elm in soup.find_all('h2',class_='supports')]

bands = sum(bands_split,[])

all_bands = list(set(bands+supports))

print "Upcoming bands playing around Boston."

for band in all_bands:
    print band
print
print "Adding TOP 3 songs of each band to a Spotify playlist..."
all_tracks = []
for band in all_bands:
    try:
        if len(band) != 0:
            search = session.search(str(band))
            search.load()
            if len(search.tracks) > 0:
                # take the top 5 tracks
                for i,track in enumerate(search.tracks):
                    if i <= 2:
                        all_tracks.append(track)
    except UnicodeEncodeError:
        print "UNICODE ERROR - Can't add:",band

# check if you've already made this playlist before
exists = False
for i,playlisti in enumerate(session.playlist_container):
    print playlisti.name
    if "Upcoming LIVE Boston Music" in playlisti.name:
        exists = True
        playlisti.remove_tracks(np.arange(len(playlisti.tracks)))
        print "Playlist already exists - removing and updating with new tracks!"

if not exists:
    print "Adding %i band, totalling %i tracks!" % (len(all_bands),len(all_tracks))
    session.playlist_container.add_new_playlist("Upcoming LIVE Boston Music")
    playlisti = session.playlist_container[-1]

print "Adding tracks to:",playlisti.name
playlisti.add_tracks(all_tracks)
playlisti.load()

session.logout()

print
print "Check your new playlist soon!"

