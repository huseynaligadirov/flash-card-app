import json
class DataManager:
    filename='files/data.json'
    def saveData(self, data):
        with open(self.filename, 'w') as json_file:
            json.dump(data, json_file)