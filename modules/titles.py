import random, string
from modules.zalgo import encrypt_text

def random_string(length=16):
    """Генерирует случайную строку из букв."""
    return ''.join(random.choices(string.ascii_letters, k=length))

def make_title(title: str, length=16):
    return f'{random_string(4)} [       {encrypt_text(title)}       ] {random_string(32)}'
