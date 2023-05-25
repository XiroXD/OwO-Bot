import json


def get(field):
    config = json.loads(open('config/config.json').read())
    return config[field]

def set(field, value):
    config = json.loads(open('config/config.json').read())
    config[field] = value
    json.dump(config, open('config/config.json', 'w'), indent=4)
