import webbrowser

def open_browser(url="https://www.google.com"):
    """Открывает веб-браузер с указанным URL."""
    try:
        webbrowser.open(url)
        return f"Браузер открыт с URL: {url}"
    except Exception as e:
        return f"Ошибка открытия браузера: {e}"
