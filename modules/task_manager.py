import psutil
from .logger import *

def get_process_list():
    """Возвращает список активных процессов."""
    processes = []
    for proc in psutil.process_iter(attrs=["pid", "name", "status"]):
        processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Status: {proc.info['status']}")
    return processes

def parse_process_info(text):
    # Разделяем текст на пары ключ-значение
    parts = text.split(", ")

    # Инициализируем переменные
    pid = None
    name = None
    status = None

    # Обрабатываем каждую пару
    for part in parts:
        key, value = part.split(": ", 1)
        key = key.strip().lower()  # Приводим ключ к нижнему регистру
        value = value.strip()

        if key == "pid":
            pid = int(value)  # Преобразуем PID в число
        elif key == "name":
            name = value
        elif key == "status":
            status = value

    return pid, name, status

def kill_process(pid):
    """Завершает процесс по PID."""
    try:
        p = psutil.Process(pid)
        p.terminate()
        msg = f"Процесс {pid} ({p.name()}) завершен."
        log(msg)
        return msg
    except Exception as e:
        msg = f"Ошибка завершения процесса {pid}: {e}"
        log(msg, ERROR)
        return msg
    
import psutil

def suspend_process(pid):
    """
    Приостанавливает процесс с указанным PID.

    :param pid: ID процесса, который нужно приостановить.
    :return: Строка с результатом выполнения операции.
    """
    try:
        process = psutil.Process(pid)
        process.suspend()
        msg = f"Процесс с PID {pid} успешно приостановлен."
        log(msg)
        return msg
    except psutil.NoSuchProcess:
        msg = f"Ошибка: Процесс с PID {pid} не существует."
        log(msg, ERROR)
        return msg
    except psutil.AccessDenied:
        msg = f"Ошибка: Доступ к процессу с PID {pid} запрещён."
        log(msg, ERROR)
        return msg
    except Exception as e:
        msg = f"Ошибка при приостановке процесса с PID {pid}: {e}"
        log(msg, ERROR)
        return msg

def resume_process(pid):
    """
    Возобновляет приостановленный процесс с указанным PID.

    :param pid: ID процесса, который нужно возобновить.
    :return: Строка с результатом выполнения операции.
    """
    try:
        process = psutil.Process(pid)
        process.resume()
        msg = f"Процесс с PID {pid} успешно возобновлён."
        log(msg)
        return msg
    except psutil.NoSuchProcess:
        msg = f"Ошибка: Процесс с PID {pid} не существует."
        log(msg, ERROR)
        return msg
    except psutil.AccessDenied:
        msg = f"Ошибка: Доступ к процессу с PID {pid} запрещён."
        log(msg, ERROR)
        return msg
    except Exception as e:
        msg = f"Ошибка при возобновлении процесса с PID {pid}: {e}"
        log(msg, ERROR)
        return msg

