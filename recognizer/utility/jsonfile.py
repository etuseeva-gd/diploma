import json


def read_json(path):
    file = open(path)
    data = json.load(file)
    file.close()
    return data


def write_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
