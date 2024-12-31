import subprocess

def create_restore_point():
    """Создает точку восстановления системы."""
    try:
        subprocess.run("powershell.exe -Command Checkpoint-Computer -Description 'Restore Point' -RestorePointType MODIFY_SETTINGS", shell=True, check=True)
        return "Точка восстановления успешно создана."
    except Exception as e:
        return f"Ошибка создания точки восстановления: {e}"
