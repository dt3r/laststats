# LastStats

LastStats is a Python command-line program that analyzes user's music listening data using Last.fm API.

## Features
- Get user's top artists from Last.fm API
- Get user's top tracks from Last.fm API
- Choose how many artists and tracks to retrieve
- Show artist playcount for all artists in selected limit
- Show track playcount for all tracks in selected limit
- Calculate what percentage of playcounts the top artist has
- Calculate what percentage of playcounts the top track has
- Calculate the playcount gap between top 1 artist and top 2 artist
- Interactive command-line menu for choosing which information and statistics to view
- Handle invalid user input
- Handle network and HTTP request errors

## Requirements

LastStats requires Python 3. All third-party library requirements are listed in requirements.txt.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/dt3r/laststats
```

2. Navigate into the directory (the folder is named laststats by default):

```bash
cd laststats
```

3. Install the requirements:

```bash
pip install -r requirements.txt
```

4. Copy .env.example to a new .env file:
```bash
cp .env.example .env
```

5. Open the .env file and put your API key as the value of LASTFM_API_KEY. Never commit your .env file.

## Files

- project.py - contains the main program, the LastFmUser class for retrieving data from the Last.fm API, and the functions used to calculate listening statistics.
- test_project.py - contains pytest tests for the API request handling and the statistical calculation functions.
- requirements.txt - lists the third-party Python libraries required to run and test the project.
- .env.example - provides an example of environment variable needed to store the Last.fm API key.
- .gitignore - specifies files and directories that should not be tracked by Git. Includes the .env file.
- README.md - contains instructions for installing, configuring, running, and testing LastStats, as well as it's description and design explanation.

## Usage

Run the program. It will ask for a Last.fm username and the number of artists and songs to get. If data is retrieved without any errors, an interactive menu is shown:

1. View top artists
2. View top songs
3. View formatted stats
4. Exit

### View top artists

Displays user's top artists and their playcounts, in order from highest playcount to lowest. The number of artists is limited by the limit entered by user earlier.

### View top songs

Works similarly to user's top artists, but with top songs. Ordered from song highest playcount to lowest. The limit is the same as the limit of artists.

### View formatted stats

Displays calculated and formatted statistics based on API data. 

The percentages are calculated from the playcounts within top-N results, not user's complete listening history.

### Exit 

Use to exit the program.

## Testing

The project has automated pytest tests included.

You can run the tests with:

```bash
pytest
```

The tests cover the statistics calculating functions and different API request outcomes, including successful requests, HTTP and connection errors, timeouts and other exceptions. 
API requests are mocked for testing so tests do not depend on internet connection or Last.fm API data.

## Design

LastFmUser is a class that is responsible for getting data from Last.fm API, get_data method sends requests and handles errors related with requests. The class was used in this project for separating request logic from main program. It also stores the username in the object, so there's no need for it to be passed to every API request. It also makes code easier to extend and demonstrates the concept of classes and objects in Python.

The main function is responsible for the overall program flow, user input, menu displaying and result presenting. The JSON data returned by the API is transformed into dictionaries containing artist or track names and their playcounts.
Playcounts are converted from strings returned by the API into integers so they can be summed, compared and used in percentage calculations.
Menu displaying is wrapped in a loop so the program only finishes when user wants. API requests are written before menu displaying so user waits for data fetching only one time. 
User's menu choices are handled using match case statement because it's easier to read than if/elif statements, since menu has several options.

Statistic calculating functions are separated. This makes them easier to test with pytest.
I used dictionary iterators to get the first one or two items because Last.fm API returns artists and tracks ordered from highest to lowest playcount. Therefore, the first item represents user's top artist or track.



## Attribution

This project uses data from [Last.fm.]("https://www.last.fm/")

Last.fm is a trademark of Last.fm Limited. LastStats is not affiliated with or endorsed by Last.fm.