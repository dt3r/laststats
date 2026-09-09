import pytest 
import requests
from requests.exceptions import HTTPError
from unittest.mock import Mock, patch
from project import LastFmUser, top_artists_calculations, playcount_gap, top_song_calculations


@patch("project.requests.get")
def test_api(mock_get):
    mock_response = Mock()
    user = LastFmUser("test")

    response_dict = {"topartists": {
        "artist": [
            {"name": "test_band_1", "playcount": "150"},
            {"name": "test_band_2", "playcount": "90"},
            {"name": "test_band_3", "playcount": "50"}
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
    test_dictionary = {"test_band_1": 50,
                   "test_band_2": 25,
                     "test_band_3": 25
                     }
    
    test_dictionary_2 = {"test_band_1": 100,
                     }
    
    test_dictionary_3 = {"test_band_1": 30,
                   "test_band_2": 20,
                     "test_band_3": 20,
                     "test_band_4": 20,
                     "test_band_5": 10 
                     }
    
    test_dictionary_4 = {"test_band_1": 25,
                   "test_band_2": 21,
                     "test_band_3": 20,
                     "test_band_4": 20,
                     "test_band_5": 20 
                     }

    
    assert top_artists_calculations(test_dictionary) == "test_band_1 dominates your listening, you listen to them 50% of time! 50 plays"
    assert top_artists_calculations(test_dictionary_2) == "You're obsessed with test_band_1, you only listen to their tracks! 100 plays"
    assert top_artists_calculations(test_dictionary_3) == "test_band_1 is your clear favourite, 30% from your total playcount! 30 plays"
    assert top_artists_calculations(test_dictionary_4) == "Your music taste is diverse! test_band_1 is your #1 artist and they only take 24% from your total playcount. 25 plays"

def test_playcount_gap():
    test_dictionary = {"test_band_1": 50,
                       "test_band_2": 40,                        
                         }

    test_dictionary_2 = {"test_band_1": 50,
                       "test_band_2": 41,                        
                         }

    test_dictionary_3 = {"test_band_1": 50,
                           "test_band_2": 20,                        
                             }
    
    test_dictionary_4 = {"test_band_1": 200,
                            "test_band_2": 100,                        
                              }
    
    test_dictionary_5 = {"test_band_1": 200,
                            "test_band_2": 20,                        
                              }
    
    test_dictionary_6 = {"test_band_1": 550,
                            "test_band_2": 100,                        
                              }
    
    test_dictionary_7 = {"test_band_1": 1000,
                            "test_band_2": 200,                        
                              }
    

    test_dictionary_8 = {"test_band_1": 50,
                       "test_band_2": 50,                        
                         }

    assert playcount_gap(test_dictionary) == "test_band_2 is only 10 plays away from test_band_1, your taste is concentrated!"
    assert playcount_gap(test_dictionary_2) == "test_band_2 is only 9 plays away from test_band_1, your taste is concentrated!"

    assert playcount_gap(test_dictionary_3) == "test_band_2 is really close to test_band_1, the gap is 30 plays!"
    assert playcount_gap(test_dictionary_4) == "test_band_2 is really close to test_band_1, the gap is 100 plays!"

    assert playcount_gap(test_dictionary_5) == "test_band_2 is 180 plays away from test_band_1!"
    assert playcount_gap(test_dictionary_6) == "test_band_2 is 450 plays away from test_band_1!"
    assert playcount_gap(test_dictionary_7) == "test_band_2 can't compete with your favourite artist, they are 800 plays away from test_band_1!"
    assert playcount_gap(test_dictionary_8) is None

def test_top_song_calculations():
  test_dictionary = {"test_song_1": 30,
                     "test_song_2": 20,                   
                       }

  test_dictionary_2 = {"test_song_1": 21123,
                     "test_song_2": 8323,                   
                       }

  test_dictionary_3 = {"test_song_1": 21123,
                       "test_song_2": 8323,    
                       "test_song_3": 2414,
                       "test_song_4": 1390,
                       "test_song_5": 444               
                         }
  
  assert top_song_calculations(test_dictionary) == "Your favourite song is test_song_1, it stands for 60% plays from your total playcount!"
  assert top_song_calculations(test_dictionary_2) == "Your favourite song is test_song_1, it stands for 72% plays from your total playcount!"
  assert top_song_calculations(test_dictionary_3) == "Your favourite song is test_song_1, it stands for 63% plays from your total playcount!"
  ...
