import psutil

def get_process_list():
    """Возвращает список активных процессов."""
    processes = []
    for proc in psutil.process_iter(attrs=["pid", "name", "status"]):
        processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Status: {proc.info['status']}")
    return processes

def kill_process(pid):
    """Завершает процесс по PID."""
    try:
        p = psutil.Process(pid)
        p.terminate()
        return f"Процесс {pid} ({p.name()}) завершен."
    except Exception as e:
        return f"Ошибка завершения процесса {pid}: {e}"
