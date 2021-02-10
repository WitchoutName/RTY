import json


class Data:
    def __init__(self):
        self.data = {}
        self.get_data()

    def get_data(self):
        with open("data.json", "r") as file:
            self.data = json.load(file)

    def save_data(self):
        with open("data.json", "w") as file:
            json.dump(self.data, file)