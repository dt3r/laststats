import os
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv("LASTFM_API_KEY")
URL = "https://ws.audioscrobbler.com/2.0/"

class LastFmUser:
    # Class for retrieving information from Last.fm API

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

        # Timeout is needed so the program doesn't hang indefinitely.
        try:
            response = requests.get(url=URL, params=params, timeout=10)
            
            response.raise_for_status()
            
            return response.json()
        
        except HTTPError as http_e:
            status_code = http_e.response.status_code
            print(f"HTTP error (Status code: {status_code}).")

        except ConnectionError:
            print("Connection error. Check your internet connection.")

        except requests.exceptions.Timeout:
            print("The server took too long to answer.")
        
        except requests.exceptions.RequestException as e:
            print(f"An error occured: {e}")

        
def main():
    username = input("Enter Last.fm username: ")
    user = LastFmUser(username)

    top_artists_data = user.get_data(method="user.getTopArtists", limit=15)

    # Creates two dictionaries because we may need to work with playcount in the future.
    # I converted the playcounts of both dictionaries to int because API returns playcount as str.

    artists = top_artists_data["topartists"]["artist"]
    artist_plays = {artist["name"]: int(artist["playcount"]) for artist in artists} 

    for artist, plays in artist_plays.items():
        print(f"{artist}: {plays} plays")


    
    data_top_tracks = user.get_data(method="user.getTopTracks", limit=15)
    
    tracks = data_top_tracks["toptracks"]["track"]
    track_plays = {track["name"]: int(track["playcount"]) for track in tracks}

    for track, plays in track_plays.items():
            print(f"{track}: {plays} plays")



    print("\nData provided by Last.fm")
    print("https://www.last.fm/\n")

def total_playcount():
    ...



if __name__ == "__main__":
    main()