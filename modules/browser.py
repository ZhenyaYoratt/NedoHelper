from webbrowser import open as webopen

from .logger import *

def open_browser(url="https://www.google.com"):
    """Открывает веб-браузер с указанным URL."""
    try:
        webopen(url)
        msg = f"Браузер открыт с URL: {url}"
        log(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка открытия браузера: {e}"
        log(msg, ERROR)
        return msg
