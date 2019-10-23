import os
import requests
from requests.exceptions import HTTPError
# api_key = '1033d244'
API_KEY = os.environ.get('API_KEY')


def get_movie_data(movie):
    """
    Accessing OMDb by API to get movie by it's title
    :param movie: str
    :return: dict
    """
    headers = {'accept': 'application/json'}
    try:
        result = requests.get(f'http://www.omdbapi.com/?apikey={API_KEY}&t={movie}', headers)
        return result.json()
    except HTTPError as error:
        return error
