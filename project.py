import os
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv

load_dotenv() 

api_key = os.getenv("LASTFM_API_KEY")
url = "http://ws.audioscrobbler.com/2.0/"

def main():
    username = input("Enter Last.fm username: ")

    try:
        top_artists_data = get_top_artists(username)
    except HTTPError as e:
        print(f"Error: {e}")
        return

    artists = top_artists_data["topartists"]["artist"]

    artist_plays = {artist["name"]: artist["playcount"] for artist in artists} 
    for artist, plays in artist_plays.items():
        print(f"{artist}: {plays} plays")

    print("\nData provided by Last.fm")
    print("https://www.last.fm/\n")
    

    
def get_top_artists(username):
    params = {
        "method": "user.getTopArtists",
        "user": username,
        "api_key": api_key,
        "format": "json",
        "limit": 10
    } 

    response = requests.get(url=url, params=params, timeout=10)

    response.raise_for_status()

    return response.json()
    


if __name__ == "__main__":
    main()