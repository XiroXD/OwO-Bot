from colorama import Fore, Back, Style


def warn(text):
    return print(f'{Back.YELLOW}{Fore.BLACK}[WARN]{Back.RESET} {Fore.YELLOW}{text}')


def error(text):
    return print(f'{Back.RED}{Fore.BLACK}[ERROR]{Back.RESET} {Fore.RED}{text}')


def info(text):
    return print(f'{Back.CYAN}{Fore.BLACK}[INFO]{Back.RESET} {Fore.BLUE}{text}')


def success(text):
    return print(f'{Back.GREEN}{Fore.BLACK}[SUCCESS]{Back.RESET} {Fore.GREEN}{text}')


def custom_info(prefix, text):
    return print(f'{Back.CYAN}{Fore.BLACK}{prefix}{Back.RESET} {Fore.BLUE}{text}')

def print_banner():
    banner = """
  _____         _____     ______             
 / ___ \       / ___ \   (____  \       _    
| |   | |_ _ _| |   | |   ____)  ) ___ | |_  
| |   | | | | | |   | |  |  __  ( / _ \|  _) 
| |___| | | | | |___| |  | |__)  ) |_| | |__ 
 \_____/ \____|\_____/   |______/ \___/ \___)
                                             
"""

    print(Fore.BLUE + Style.BRIGHT + banner)
