import pytest 
import requests
from requests.exceptions import HTTPError
from unittest.mock import Mock, patch
from project import LastFmUser, top_artists_calculations, playcount_gap


@patch("project.requests.get")
def test_api(mock_get):
    mock_response = Mock()
    user = LastFmUser("test")

    response_dict = {"topartists": {
        "artist": [
            {"name": "Metallica", "playcount": "150"},
            {"name": "Nirvana", "playcount": "90"},
            {"name": "Weezer", "playcount": "50"}
            ]
            }
            }

    mock_response.json.return_value = response_dict

    mock_get.return_value = mock_response
    response = user.get_data(method="user.getTopArtists", limit=3)
    
    assert response == response_dict

@patch("project.requests.get")
def test_http_error(mock_get):
    mock_response = Mock()

    http_error = HTTPError()
    http_error.response = Mock()
    http_error.response.status_code = 404

    mock_response.raise_for_status.side_effect = http_error
    mock_get.return_value = mock_response

    user = LastFmUser("test")
    result = user.get_data(method="user.getTopArtists")

    assert result is None

@patch("project.requests.get")
def test_connection_error(mock_get):
    mock_get.side_effect = ConnectionError()
    
    user = LastFmUser("test")
    result = user.get_data(method="user.getTopArtists")
    
    assert result is None

@patch("project.requests.get")
def test_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()
    
    user = LastFmUser("test")
    result = user.get_data(method="user.getTopArtists")
    
    assert result is None

@patch("project.requests.get")
def test_request_exception(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException()

    user = LastFmUser("test")
    result = user.get_data(method="user.getTopArtists")

    assert result is None

def test_top_artists_calculations():
    test_dictionary = {"Metallica": 50,
                   "Nirvana": 25,
                     "Weezer": 25
                     }
    
    test_dictionary_2 = {"Metallica": 100,
                     }
    
    test_dictionary_3 = {"Metallica": 30,
                   "Nirvana": 20,
                     "Weezer": 20,
                     "Pink Floyd": 20,
                     "AC/DC": 10 
                     }
    
    test_dictionary_4 = {"Metallica": 25,
                   "Nirvana": 21,
                     "Weezer": 20,
                     "Pink Floyd": 20,
                     "AC/DC": 20 
                     }

    
    assert top_artists_calculations(test_dictionary) == "Metallica dominates your listening, you listen to them 50% of time! 50 plays"
    assert top_artists_calculations(test_dictionary_2) == "You're obsessed with Metallica, you only listen to their tracks! 100 plays"
    assert top_artists_calculations(test_dictionary_3) == "Metallica is your clear favourite, 30% from your total playcount! 30 plays"
    assert top_artists_calculations(test_dictionary_4) == "Your music taste is diverse! Metallica is your #1 artist and they only take 24% from your total playcount. 25 plays"

def test_playcount_gap():
    test_dictionary = {"Metallica": 50,
                       "Nirvana": 40,                        
                         }

    test_dictionary_2 = {"Metallica": 50,
                       "Nirvana": 41,                        
                         }

    test_dictionary_3 = {"Metallica": 50,
                           "Nirvana": 20,                        
                             }
    
    test_dictionary_4 = {"Metallica": 200,
                            "Nirvana": 100,                        
                              }
    
    test_dictionary_5 = {"Metallica": 200,
                            "Nirvana": 20,                        
                              }
    
    test_dictionary_6 = {"Metallica": 550,
                            "Nirvana": 100,                        
                              }
    
    test_dictionary_7 = {"Metallica": 1000,
                            "Nirvana": 200,                        
                              }
    

    test_dictionary_8 = {"Metallica": 50,
                       "Nirvana": 50,                        
                         }

    assert playcount_gap(test_dictionary) == "Nirvana is only 10 plays away from Metallica, your taste is concentrated!"
    assert playcount_gap(test_dictionary_2) == "Nirvana is only 9 plays away from Metallica, your taste is concentrated!"

    assert playcount_gap(test_dictionary_3) == "Nirvana is really close to Metallica, the gap is 30 plays!"
    assert playcount_gap(test_dictionary_4) == "Nirvana is really close to Metallica, the gap is 100 plays!"

    assert playcount_gap(test_dictionary_5) == "Nirvana is 180 plays away from Metallica!"
    assert playcount_gap(test_dictionary_6) == "Nirvana is 450 plays away from Metallica!"
    assert playcount_gap(test_dictionary_7) == "Nirvana can't compete with your favourite artist, they are 800 plays away from Metallica!"
    assert playcount_gap(test_dictionary_8) is None