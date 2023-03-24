🎵 Local Live Music
=================


Just Give Me The Playlists
=========

Click on any of the following:


About
=====

I wanted a way to get more live music outside of The AlgorithmTM echo chamber. This is the result.

This code updates playlists in Spotify based on upcoming music found in your local area.
The data source is [Bands In Town](https://www.bandsintown.com/). It should capture most bands, but maybe not all. If there is ambiguity over a band name for instance, it may mistakenly put the wrong band in the playlist -- sorry about that.

It should be rare and so the overwhelming majority are bands playing LIVE near you soon. Enjoy =)

<table>
  <tr>
    <td><a href="https://open.spotify.com/playlist/3PjTtXAvsLe3C59USzfkni?si=54a5eb05b5d84d99"><img src="playlist_brisbane.png" style="width:100%"></a></td>
    <td><a href="https://open.spotify.com/playlist/4ctDUQ505YnGNoj21yYpxI?si=54a5eb05b5d84d99"><img src="playlist_melbourne.png" style="width:100%"></a></td>
  </tr>
  <tr>
    <td><a href="https://open.spotify.com/playlist/1Shh4ljWPQrcsvpTKtppm5?si=54a5eb05b5d84d99"><img src="playlist_sydney.png" style="width:100%"></a></td>
    <td><a href="https://open.spotify.com/playlist/5FsF0m0y3J8DT9t5APliQH?si=54a5eb05b5d84d99"><img src="playlist_adelaide.png" style="width:100%"></a></td>
  </tr>
</table>


Requirements
============
* Spotify
* [spotipy](https://spotipy.readthedocs.io/en/2.22.1/)

Also set these environment variables in your `~/.bashrc` or whichever you're using. You can get these from Spotfiy [here](https://developer.spotify.com/dashboard/applications) but you also need to click "Edit Settings" for your app and add the redirect uri below:

```bash
export SPOTIFY_CLIENT_ID='SPOTIPY_CLIENT_ID'
export SPOTIFY_CLIENT_SECRET='SPOTIPY_CLIENT_SECRET'
export SPOTIFY_REDIRECT_URI='http://localhost:8899/callback'
export SPOTIFY_CLIENT_PLAYLISTID='SPOTIFY_CLIENT_PLAYLISTID'
export SPOTIFY_USER_ID='SPOTIFY_USER_ID'
```

Running
======

Once you have made the correct modifications, in `getlocalbands.py` and added those environment variables, you can just run:

```Python
python getlocalbands.py
```

Ideally you run this in concept, not in actuality as it just duplicates what is already available. =)

Tested On
=========
Tested on Mac OS X 13.2.1 Ventura with Python 3.8. This should work on other
platforms, however.

