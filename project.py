import os
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv("LASTFM_API_KEY")
URL = "https://ws.audioscrobbler.com/2.0/"

class LastFmUser:
    def __init__(self, username):
        self.username = username

    def get_data(self, method: str, limit: int = 10):
        params = {
            "method": method,
            "user": self.username,
            "api_key": API_KEY,
            "format": "json",
            "limit": limit
        } 
        response = requests.get(url=URL, params=params, timeout=10)
        
        response.raise_for_status()
        
        return response.json()

def main():
    username = input("Enter Last.fm username: ")
    user = LastFmUser(username)

    try:
        top_artists_data = user.get_data(method="user.getTopArtists", limit=15)
    except HTTPError as e:
        print(f"Error: {e}")
        return

    artists = top_artists_data["topartists"]["artist"]
    artist_plays = {artist["name"]: int(artist["playcount"]) for artist in artists} 

    for artist, plays in artist_plays.items():
        print(f"{artist}: {plays} plays")




    try:
        data_top_tracks = user.get_data(method="user.getTopTracks", limit=15)
    except HTTPError as e:
        print(f"Error: {e}")
        return
    
    tracks = data_top_tracks["toptracks"]["track"]
    track_plays = {track["name"]: int(track["playcount"]) for track in tracks}

    for track, plays in track_plays.items():
            print(f"{track}: {plays} plays")



    print("\nData provided by Last.fm")
    print("https://www.last.fm/\n")




if __name__ == "__main__":
    main()