import random
import json
import time

from typing import Sequence
from utils import Api, Log
while True:
    try:
        with open("config/config.json") as f:
            config = json.load(f)
            owofied = config["owofied"]
            prefix = config["prefix"]

        with open("data/version.json") as f:
            config = json.load(f)
            version = config["version"]
            build = config["build"]
        break
    except FileNotFoundError:
        Api.get_version()
        time.sleep(1)
    except Exception as e:
        Log.error(e)
        break


def codeblock(title: str, text: str):
    if owofied:
        title = owofy(title)
        text = owofy(text)

    return f"""
```ini
[OwO Bot {version}]
```
```ini
[{title}]
        
{text}
```
```
OwO Bot - Made by Xiro#0001 | Prefix: {prefix} | Build: {build}
```
"""


def paginated_codeblock(title: str, text: str, page: int, num_pages: int):
    if owofied:
        title = owofy(title)
        text = owofy(text)

    return f"""
```ini
[OwO Bot {version}]
```
```ini
{text}
    
[{title} (page {page}/{num_pages})]
```
```
OwO Bot - Made by Xiro#0001 | Prefix: {prefix} | Build: {build}
```
"""


def error(message: str):
    return f"""
```ini
[OwO Bot]

[Error] {message} 
```
    """


# Source: https://github.com/Makiyu-py/humor_langs/blob/master/humor_langs/main_trans.py#LL6C1-L6C1
def owofy(text: Sequence, *, wanky: bool = False, _print: bool = False):
    # sourcery skip: swap-if-expression
    """translates your given text to owo!

    :param text: the string/array you want to translate to owo on
    :type text: typing.Sequence
    :param wanky: A boolean that represents if you want the word 'wank' in your translated text. Defaults to `False`
    :type wanky: bool
    :param _print: If you want to print the given output. Defaults to `False`
    :type _print: bool
    :return: Your requested, translated text in str/array/printed form!
    :rtype: Union[str, list, print()]
    """

    def last_replace(s, old, new):
        li = s.rsplit(old, 1)
        return new.join(li)

    def text_to_owo(textstr):
        exclamations = ("?", "!", ".", "*")

        prefixes = [
            "Haii UwU ",
            "Hiiiiii 0w0 ",
            "Hewoooooo >w< ",
            "*W* ",
            "mmm~ uwu ",
            "Oh... Hi there {} ".format(random.choice(["·///·", "(。O⁄ ⁄ω⁄ ⁄ O。)"])),
        ]  # I need a life, help me

        subs = {
            "why": "wai",
            "Why": "Wai",
            "Hey": "Hai",
            "hey": "hai",
            "ahw": "ao",
            "Hi": "Hai",
            "hi": "hai",
            "you": "u",
            "L": "W",
            "l": "w",
            "R": "W",
            "r": "w",
        }

        textstr = random.choice(prefixes) + textstr
        if not textstr.endswith(exclamations):
            textstr += " uwu"

        smileys = [";;w;;", "^w^", ">w<", "UwU", r"(・`ω\´・)"]

        if not wanky:  # to prevent wanking * w *
            textstr = textstr.replace("Rank", "Ⓡank").replace("rank", "Ⓡank")
            textstr = textstr.replace("Lank", "⒧ank").replace("lank", "⒧ank")

        textstr = last_replace(textstr, "there!", "there! *pounces on u*")

        for key, val in subs.items():
            textstr = textstr.replace(key, val)

        textstr = last_replace(textstr, "!", "! {}".format(random.choice(smileys)))
        textstr = last_replace(
            textstr, "?", "? {}".format(random.choice(["owo", "O·w·O"]))
        )
        textstr = last_replace(textstr, ".", ". {}".format(random.choice(smileys)))

        vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]

        if not wanky:
            textstr = textstr.replace("Ⓡank", "rank").replace("⒧ank", "lank")

        for v in vowels:
            if "n{}".format(v) in textstr:
                textstr = textstr.replace("n{}".format(v), "ny{}".format(v))
            if "N{}".format(v) in textstr:
                textstr = textstr.replace(
                    "N{}".format(v), "N{}{}".format("Y" if v.isupper() else "y", v)
                )

        return textstr

    if not isinstance(text, str):
        owoed_msgs = map(text_to_owo, text)

        return owoed_msgs if not _print else print(*owoed_msgs, sep="\n")

    return text_to_owo(text) if not _print else print(text_to_owo(text))
