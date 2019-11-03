import requests
from requests.exceptions import HTTPError
API_KEY = ''  # please put in here your omdb api key
# API_KEY = os.environ.get('API_KEY')


def get_movie_data(movie):
    """
    Accessing OMDb by API to get movie by it's title
    :param movie: str
    :return: dict
    """
    headers = {'accept': 'application/json'}
    try:
        result = requests.get(f'http://www.omdbapi.com/?apikey={API_KEY}&t={movie}&type=movie', headers).json()
        if result['Response'] == 'False':
            return False, f'Could not find movie named "{movie}". Please check spelling.'
        return result
    except HTTPError as error:
        return error


if __name__ == '__main__':

    print(get_movie_data('Kac Wawa'))
