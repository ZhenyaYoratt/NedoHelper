import ctypes

def set_wallpaper(image_path):
    """Устанавливает обои рабочего стола."""
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        return "Обои успешно установлены."
    except Exception as e:
        return f"Ошибка установки обоев: {e}"

def reset_wallpaper():
    """Сбрасывает обои рабочего стола на дефолтный цвет."""
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, "", 3)
        return "Обои сброшены."
    except Exception as e:
        return f"Ошибка сброса обоев: {e}"
