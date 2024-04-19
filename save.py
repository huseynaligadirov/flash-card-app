import json
import os

class DataManager:
    filename='files/data.json'

    def init(self):
        if os.path.exists(self.filename):
            return self.__readData()
        else:
            template = {
                "translations": {},
                "progress": {}
            }
            self.saveData(template)
            return template

    def saveData(self, data):
        with open(self.filename, 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file)

    def __readData(self):
        with open(self.filename, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

data_manager = DataManager()