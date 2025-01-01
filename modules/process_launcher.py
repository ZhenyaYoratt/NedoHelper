import subprocess
from .logger import *

def launch_process(command, admin=False):
    """Запускает процесс с опциональными правами администратора."""
    try:
        if admin:
            subprocess.run(command, shell=True)
        else:
            subprocess.Popen(command, shell=True)
        return f"Процесс '{command}' успешно запущен."
    except Exception as e:
        msg = f"Ошибка запуска процесса '{command}': {e}"
        log(msg, ERROR)
        return msg