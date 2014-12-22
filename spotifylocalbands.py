import requests
import bs4
import spotify
import sys

"""
Contact: Brendan Griffen brendan.f.griffen@gmail.com @brendangriffen

Code will scrape bands playing in next few months in Boston area.

Requirements:

libspotify:     https://developer.spotify.com/technologies/libspotify/
pyspotify:      https://github.com/mopidy/pyspotify
developer key:  https://devaccount.spotify.com/my-account/keys/

Enjoy the tunes!

"""

session = spotify.Session()
session.login('username', 'password')

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

# try a few times to connect
for i in xrange(0,5):
    session.process_events()

print
print "Adding TOP 3 songs of each band to a Spotify playlist..."
all_tracks = []
for band in all_bands:
    if len(band) != 0:
        search = session.search(str(band))
        search.load()
        if len(search.tracks) > 0:
            # take the top 5 tracks
            for i,track in enumerate(search.tracks):
                if i <= 2:
                    all_tracks.append(track)


# check if you've already made this playlist before
#exists = False
#for i,playlisti in enumerate(session.playlist_container):
#    print playlisti.name
#    if "Boston" in playlisti.name:
#        idx_playlist = i
#        exists = True
#        print "Playlist already exists - updating!"

# remove it if you have already made the playlist before
#if exists:
#    session.playlist_container.remove(idx_playlist)

#----------

print "Adding %i band, totalling %i tracks!" % (len(all_bands),len(all_tracks))
session.playlist_container.add_new_playlist("Upcoming LIVE Boston Music")
playlist = session.playlist_container[-1]

print "Adding tracks to:",playlist.name
playlist.add_tracks(all_tracks)
playlist.load()

session.logout()

print
print "Check your new playlist soon!"

