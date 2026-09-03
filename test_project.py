import pytest 
import requests
from requests.exceptions import HTTPError
from unittest.mock import Mock, patch
from project import LastFmUser


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
