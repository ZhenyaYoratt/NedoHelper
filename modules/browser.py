import webbrowser

from logger import log

def open_browser(url="https://www.google.com"):
    """Открывает веб-браузер с указанным URL."""
    try:
        webbrowser.open(url)
        msg = f"Браузер открыт с URL: {url}"
        log(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка открытия браузера: {e}"
        log(msg, 'error')
        return msg
