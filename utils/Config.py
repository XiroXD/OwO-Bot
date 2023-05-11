import json


def get():
    return json.loads(open('config/config.json').read())
