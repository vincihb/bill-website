import json
from os import path


class ConfReader:
    _local_dir = path.dirname(path.abspath(__file__))
    CONFIG_INDEX = path.join(_local_dir, 'index.json')

    def __init__(self):
        with open(self.CONFIG_INDEX) as json_file:
            data = json.load(json_file)
            self.NEWS_API_KEY = data['NEWS_API_KEY']
            self.PROPUBLICA_API_KEY = data['PROPUBLICA_API_KEY']
            self.PORT = data['PORT']
            self.CURRENT_CONGRESS = data['CURRENT_CONGRESS']


conf = ConfReader()
