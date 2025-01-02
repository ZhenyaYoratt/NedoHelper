import subprocess
from .logger import *

def launch_process(command):
    """Запускает процесс с опциональными правами администратора."""
    try:
        subprocess.Popen(command, shell=True)
        return f"Процесс '{command}' успешно запущен."
    except Exception as e:
        msg = f"Ошибка запуска процесса '{command}': {e}"
        log(msg, ERROR)
        return msg