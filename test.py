import json

data = {"Hola2": 1}

with open('data.json', 'a+') as file:
    json.dump(data, file)