import subprocess
from modules.logger import *

def list_users():
    """Получает список пользователей в системе."""
    try:
        result = subprocess.run(["net", "user"], capture_output=True, encoding="utf8", check=True)
        print(result.stdout)
        print(result.stdout.encode())
        lines = result.stdout.split("\n")
        start_index = next(i for i, line in enumerate(lines) if "-----" in line) + 1
        end_index = next(i for i, line in enumerate(lines[start_index:], start=start_index) if not line.strip())
        users = "\n".join(line.strip() for line in lines[start_index:end_index])
        return f"Пользователи:\n{users}"
    except Exception as e:
        msg = f"Ошибка получения списка пользователей: {e}"
        log(msg, ERROR)
        return msg

def add_user(username, password):
    """Добавляет нового пользователя с паролем."""
    try:
        subprocess.run(["net", "user", username, password, "/add"], check=True)
        msg = f"Пользователь {username} успешно добавлен."
        log(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка добавления пользователя {username}: {e}"
        log(msg, ERROR)
        return msg

def delete_user(username):
    """Удаляет пользователя из системы."""
    try:
        subprocess.run(["net", "user", username, "/delete"], check=True)
        msg = f"Пользователь {username} успешно удалён."
        log(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка удаления пользователя {username}: {e}"
        log(msg, ERROR)
        return msg

def set_password(username, password):
    """Устанавливает пароль для пользователя."""
    try:
        subprocess.run(["net", "user", username, password], check=True)
        msg = f"Пароль для пользователя {username} успешно установлен."
        log(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка установки пароля для пользователя {username}: {e}"
        log(msg, ERROR)
        return msg

def remove_password(username):
    """Удаляет пароль у пользователя."""
    try:
        subprocess.run(["net", "user", username, "*"], input="\n", text=True, check=True)
        msg = f"Пароль для пользователя {username} успешно удалён."
        log(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка удаления пароля для пользователя {username}: {e}"
        log(msg, ERROR)
        return msg
