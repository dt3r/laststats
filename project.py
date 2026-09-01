import os
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv

load_dotenv() 

api_key = os.getenv("LASTFM_API_KEY")
url = "https://ws.audioscrobbler.com/2.0/"

def main():
    username = input("Enter Last.fm username: ")


    try:
        top_artists_data = lastfm_get(username, method="user.getTopArtists", limit=15)
    except HTTPError as e:
        print(f"Error: {e}")
        return

    artists = top_artists_data["topartists"]["artist"]
    artist_plays = {artist["name"]: int(artist["playcount"]) for artist in artists} 

    for artist, plays in artist_plays.items():
        print(f"{artist}: {plays} plays")




    try:
        data_top_tracks = lastfm_get(username, method="user.getTopTracks", limit=15)
    except HTTPError as e:
        print(f"Error: {e}")
        return
    
    tracks = data_top_tracks["toptracks"]["track"]
    track_plays = {track["name"]: int(track["playcount"]) for track in tracks}

    for track, plays in track_plays.items():
            print(f"{track}: {plays} plays")




    try:
        top_tags_data = lastfm_get(username, method="user.getTopTags", limit=15)
    except HTTPError as e:
        print(f"Error: {e}")
        return

    tags = top_tags_data["toptags"]["tag"]

    for tag in tags:
        print(f"{tag['name']}")



    print("\nData provided by Last.fm")
    print("https://www.last.fm/\n")



def lastfm_get(username, method, limit: int = 10):
    params = {
        "method": method,
        "user": username,
        "api_key": api_key,
        "format": "json",
        "limit": limit 
    } 

    response = requests.get(url=url, params=params, timeout=10)

    response.raise_for_status()

    return response.json()





if __name__ == "__main__":
    main()