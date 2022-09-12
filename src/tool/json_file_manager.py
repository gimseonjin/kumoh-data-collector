import json


class JsonFileManager():

    def __init__():
        pass

    def read_data_from_local(file_path:str):
        with open(file_path, 'rt', encoding='UTF-8') as file:
            data = json.load(file)
        return data

    def save_data_in_local(file_path:str, data_list:list):
        with open(file_path, 'w') as file:
            json.dump(data_list, file)