from random import choices, randint
from string import ascii_letters
#from modules.zalgo import encrypt_text

def random_string(length=16):
    """Генерирует случайную строку из букв."""
    return ''.join(choices(ascii_letters, k=length))

def make_title(title: str):
    return random_string(randint(50, 100)) #f'{random_string(4)} [       {encrypt_text(title)}       ] {random_string(32)}'
