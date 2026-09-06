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

    # Creates two dictionaries (artist_plays and track_plays) because we may need to work with playcount in the future.
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

    print(f"\n{top_artists_calculations(artist_plays)}")

    print("\nData provided by Last.fm")
    print("https://www.last.fm/\n")

def top_artists_calculations(dictionary):
    """
    Calculates favourite artist playcount to total playcount ratio.
    Returns a personalized message string based on those calculations.
    """

    total_playcount = sum(dictionary.values())
    favourite_artist = next(iter(dictionary.items()))
    favourite_artist_percent = round(favourite_artist[1] / total_playcount * 100)
    
    if favourite_artist_percent == 100:
        return f"You're obsessed with {favourite_artist[0]}, you only listen to their tracks! {favourite_artist[1]} plays"
    elif 100 > favourite_artist_percent >= 50:
        return f"{favourite_artist[0]} dominates your listening, you listen to them {favourite_artist_percent}% of time! {favourite_artist[1]} plays"
    elif 50 > favourite_artist_percent >= 25:
        return f"{favourite_artist[0]} is your clear favourite, {favourite_artist_percent}% from your total playcount! {favourite_artist[1]} plays"
    else:
        return f"Your music taste is diverse! {favourite_artist[0]} is your #1 artist and they only take {favourite_artist_percent}% from your total playcount. {favourite_artist[1]} plays"






if __name__ == "__main__":
    main()