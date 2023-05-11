import requests
import json


def nekobot_imagegen_api(endpoint: str, args: str):
    return requests.get(f"https://nekobot.xyz/api/imagegen?type={endpoint}&{args}").content


def nekobot_image_api(endpoint):
    r = json.loads(requests.get(f"https://nekobot.xyz/api/image?type={endpoint}").content)
    return r["message"]


def some_random_api(category: str, endpoint: str, args: str = None, image: bool = False, field: str = None,):
    print(f"https://some-random-api.com/{category}/{endpoint}?{args}")
    r = requests.get(f"https://some-random-api.com/{category}/{endpoint}?{args}").content
    if image:
        return r
    else:
        parsed = json.loads(r)
        return parsed[field]
