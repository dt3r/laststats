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

        # Prevent the program from hanging indefinitely if the server didn't respond.
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
    def playcount_message(dictionary):
        print()
        for name, plays in dictionary.items():
            print(f"{name}: {plays} plays")

    print("\n=======LASTSTATS=======\n")
    username = input("Enter Last.fm username: ")
    user = LastFmUser(username)

    while True:
        try:
            limit = int(input("Enter the limit of songs and/or artists: "))
            break
        except ValueError:
            print("Please enter a valid limit.")

    top_artists_data = user.get_data(method="user.getTopArtists", limit=limit)
    data_top_tracks = user.get_data(method="user.getTopTracks", limit=limit)

    # Convert API playcounts in from str to int for calculations
    if top_artists_data and data_top_tracks:
        artists = top_artists_data["topartists"]["artist"]
        artist_plays = {artist["name"]: int(artist["playcount"]) for artist in artists} 

        tracks = data_top_tracks["toptracks"]["track"]
        track_plays = {track["name"]: int(track["playcount"]) for track in tracks}

    
        while True:
            print("\n1. View top artists")
            print("2. View top songs")
            print("3. View formatted stats")
            print("4. Exit")
            while True:
                try:
                    choice = int(input("Enter your choice: "))
                    break
                except ValueError:
                    print("Input a valid choice from 1 to 4")

            match choice:
                case 1:
                    playcount_message(artist_plays)
                case 2:
                    playcount_message(track_plays)
                case 3:
                    print("\nTop artist:")
                    print(top_artists_calculations(artist_plays))
                    print(playcount_gap(artist_plays))

                    print("\nTop song:")
                    print(top_song_calculations(track_plays))               
                case 4:
                    break         

        print("\nData provided by Last.fm")
        print("https://www.last.fm/\n")
        print("=======================")

    else:
        print("\nFailed to get data from Last.fm")
    
def top_artists_calculations(dictionary):
    """
    Calculates favourite artist playcount to total artists playcount ratio.
    Returns a message string based on those calculations.
    """
    if dictionary:
        iterator = iter(dictionary.items())

        total_playcount = sum(dictionary.values())

        # Last.fm returns artists ordered by playcount, so top 1 artist is the first item
        top_1_artist = next(iterator)

        top_1_artist_percent = round(top_1_artist[1] / total_playcount * 100)

        
        if top_1_artist_percent == 100:
            return f"You're obsessed with {top_1_artist[0]}, you only listen to their tracks! {top_1_artist[1]} plays"
        elif 100 > top_1_artist_percent >= 50:
            return f"{top_1_artist[0]} dominates your listening, you listen to them {top_1_artist_percent}% of time! {top_1_artist[1]} plays"
        elif 50 > top_1_artist_percent >= 25:
            return f"{top_1_artist[0]} is your clear favourite, {top_1_artist_percent}% from your total playcount! {top_1_artist[1]} plays"
        elif 25 > top_1_artist_percent >= 0:
            return f"Your music taste is diverse! {top_1_artist[0]} is your #1 artist and they only take {top_1_artist_percent}% from your total playcount. {top_1_artist[1]} plays"

    return "Not enough data to calculate top artist stats."

def top_song_calculations(dictionary):
    """
    Calculates favourite song playcount to total songs playcount ratio.
    Returns a message string based on those calculations.
    """
    if dictionary:
        iterator = iter(dictionary.items())

        total_playcount = sum(dictionary.values())
        top_1_song = next(iterator)

        top_1_song_percent = round(top_1_song[1] / total_playcount * 100)

        return f"Your favourite song is {top_1_song[0]} ({top_1_song[1]} plays), it stands for {top_1_song_percent}% plays from all your songs!"

    return "Not enough data to calculate top song stats."
    
        
def playcount_gap(dictionary):
    """
    Calculates gap between the playcount of artist #1 and artist #2
    Returns a message string based on those calculations
    """
    if dictionary:
        dictionary_iterator = iter(dictionary.items())

        top_1_artist = next(dictionary_iterator)
        top_2_artist = next(dictionary_iterator)

        playcount_gap = top_1_artist[1] - top_2_artist[1]

        if playcount_gap == 0:
            return f"{top_2_artist[0]} shares first place with {top_1_artist[0]}"
        if 0 < playcount_gap <= 10:
            return f"{top_2_artist[0]} is only {playcount_gap} plays away from {top_1_artist[0]}, your taste is concentrated!"
        elif 10 < playcount_gap <= 100:
            return f"{top_2_artist[0]} is really close to {top_1_artist[0]}, the gap is {playcount_gap} plays!"
        elif 100 < playcount_gap <= 450:
            return f"{top_2_artist[0]} is {playcount_gap} plays away from {top_1_artist[0]}!"
        elif playcount_gap > 450:
            return f"{top_2_artist[0]} can't compete with your favourite artist, they are {playcount_gap} plays away from {top_1_artist[0]}!"
        
    return "Not enough data to calculate playcount gap."








if __name__ == "__main__":
    main()