import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def get_width():
    return os.get_terminal_size().columns