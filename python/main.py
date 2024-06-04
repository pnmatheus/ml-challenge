from call_api import get_item_data
from etl_items import etl_items_spark

if __name__ == '__main__':
    try:
        # esta função irá orquestrar a chamada da API e criação do JSON items.json
        get_item_data()
        
        # ETL do arquivo items.json com as tranformações necessárias e exportação do arquivo items.csv
        etl_items_spark()
        
    except Exception as e:
        print('Exception main: ', e)
