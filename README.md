Spotify Local Bands
=================

About
=====
Code to find upcoming bands playing locally and convert their songs into a Spotify playlist. Article I wrote about this code can be found [here](http://brendangriffen.com/blog/making-spotify-playlists-in-python-based-on-upcoming-local-bands/).

Author
======
Created by Brendan Griffen on 12/22/2014

Requirements
============
* Spotify Premium subscription
* libspotify (https://developer.spotify.com/technologies/libspotify/)
* pyspotify 2.x (https://github.com/mopidy/pyspotify)

Running
======

Once you have made the correct modifications (which could take some time if you are scraping from a different website for your area) then run the following from your terminal (assuming you have the above requirements).

```Python
python spotifylocalbands.py
```

Notes
=====
* Place spotify_appkey.key in the same directory as this file

Tested On
=========
Tested on Mac OS X 10.10.1 Yosemite with Python 2.7.8. This should work on other
platforms, however.