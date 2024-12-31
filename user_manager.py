import subprocess

def list_users():
    """Получает список пользователей в системе."""
    try:
        result = subprocess.run(["net", "user"], capture_output=True, text=True, check=True)
        lines = result.stdout.split("\n")
        start_index = next(i for i, line in enumerate(lines) if "-----" in line) + 1
        end_index = next(i for i, line in enumerate(lines[start_index:], start=start_index) if not line.strip())
        users = "\n".join(line.strip() for line in lines[start_index:end_index])
        return f"Пользователи:\n{users}"
    except Exception as e:
        return f"Ошибка получения списка пользователей: {e}"

def add_user(username, password):
    """Добавляет нового пользователя с паролем."""
    try:
        subprocess.run(["net", "user", username, password, "/add"], check=True)
        return f"Пользователь {username} успешно добавлен."
    except Exception as e:
        return f"Ошибка добавления пользователя {username}: {e}"

def delete_user(username):
    """Удаляет пользователя из системы."""
    try:
        subprocess.run(["net", "user", username, "/delete"], check=True)
        return f"Пользователь {username} успешно удалён."
    except Exception as e:
        return f"Ошибка удаления пользователя {username}: {e}"

def set_password(username, password):
    """Устанавливает пароль для пользователя."""
    try:
        subprocess.run(["net", "user", username, password], check=True)
        return f"Пароль для пользователя {username} успешно установлен."
    except Exception as e:
        return f"Ошибка установки пароля для пользователя {username}: {e}"

def remove_password(username):
    """Удаляет пароль у пользователя."""
    try:
        subprocess.run(["net", "user", username, "*"], input="\n", text=True, check=True)
        return f"Пароль для пользователя {username} успешно удалён."
    except Exception as e:
        return f"Ошибка удаления пароля для пользователя {username}: {e}"
