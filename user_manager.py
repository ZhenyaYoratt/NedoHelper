import subprocess

def list_users():
    """Возвращает список пользователей в системе."""
    try:
        result = subprocess.check_output("net user", shell=True, text=True)
        return result
    except Exception as e:
        return f"Ошибка получения списка пользователей: {e}"

def add_user(username, password):
    """Добавляет нового пользователя."""
    try:
        subprocess.run(f"net user {username} {password} /add", shell=True, check=True)
        return f"Пользователь {username} успешно добавлен."
    except Exception as e:
        return f"Ошибка добавления пользователя {username}: {e}"
