import os
import json
import definitions

def write_json(json_var: dict, file_name: str, mode: str) -> None:
    """
    Escreve um arquivo .json no diretório especificado.

    Argumentos: \n
    json_var - varivel do json, deve ser um dict \n
    file_name - diretorio do arquivo .json, deve ser uma string \n
    mode - modo de escrita do arquivo, deve ser uma string \n
    """
    try:
        JSON_PATH = os.path.join(definitions.ROOT_DIR, 'data', f'{file_name}.json')

        with open(JSON_PATH, mode, encoding='utf-8') as file:
            json.dump(json_var, file, ensure_ascii=False, indent=4)

    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    pass
