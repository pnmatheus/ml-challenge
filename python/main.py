import json
import requests
from configparser import ConfigParser

config = ConfigParser()

config.read('./conf.ini')

endpoint = config['ENDPOINTS']['SEARCH_ITEM']

print(endpoint)

def get_itens(params):
    try:
        response = requests.get(
            url=config['ENDPOINTS']['SEARCH_ITEM'],
            params=params
        )

        if response.status_code == 200:
            itens = response.json()
            return itens
    
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


if __name__ == '__main__':
    params = {'q':'chromecast', 'limit':1}

    itens = get_itens(params=params)

    for key in itens:
        print(key)
