import subprocess

def launch_process(command, admin=False):
    """Запускает процесс с опциональными правами администратора."""
    try:
        if admin:
            subprocess.run(["runas", "/user:Administrator", command], shell=True)
        else:
            subprocess.Popen(command, shell=True)
        return f"Процесс '{command}' успешно запущен."
    except Exception as e:
        return f"Ошибка запуска процесса '{command}': {e}"
