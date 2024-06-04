import requests
import json
import definitions
from utils import write_json
from configparser import ConfigParser

config = ConfigParser()

config.read(definitions.CONFIG_PATH)


def search_item(params:dict) -> list:
    """
    Retorna o response do endpoint de busca de itens.

    Argumentos: \n
    params - parametros de consulta, deve ser um dict
    """
    try:
        response = requests.get(
            url=config['endpoints']['search_item'],
            params=params
        )

        if response.status_code == 200:
            return response.json()
    
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def get_item_detail(id_item:str) -> dict:
    """
    Retorna o response do endpoint de itens.

    Argumentos: \n
    id_item - id do item, deve ser uma string
    """
    try:
        response = requests.get(
            url=f"{config['endpoints']['item_detail']}/{id_item}"
        )

        if response.status_code == 200:
            response = response.json()
            return response
    
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
def read_parameters() -> list:
    """
    Leitura dos parâmetros do arquivo params.json e retorna a lista de parâmetros.
    """
    try:
        with open(definitions.PARAMS_PATH, 'r+', encoding='utf-8') as file:
            return json.load(file)
        
    except Exception as e:
        print('Error:', e)
        return None
    

def get_item_data():
    try:
        # lê os parametros definidos no arquivo params.json
        params = read_parameters()

        # percorre os paramentos a serem consultados e realiza o metodo get no endpoint de busca
        for key, param in enumerate(params):
            response = search_item(params=param)

            if key == 0:
                search_results:list = response['results']
            else:
                for result in response['results']:
                    search_results.append(result)

        # varre os resultados do endpoint de busca e realiza o metodo get no endpoint de item
        items_list: list = []
        for key, result in enumerate(search_results):
            items:dict = get_item_detail(result['id'])
            items_list.append(items)
                
        write_json(items_list, 'items', 'w+')

    except Exception as e:
        print('Error:', e)
        return None
    
if __name__ == '__main__':
    pass
