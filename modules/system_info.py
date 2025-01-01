import psutil
from .logger import *

def get_system_info():
    """Возвращает информацию о системе."""
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    return f"CPU: {cpu_percent}%, RAM: {memory.percent}%"

def get_disk_info():
    """Возвращает информацию о дисках."""
    disk_info = psutil.disk_partitions()
    disk_data = []
    for partition in disk_info:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_data.append(f"{partition.device} ({partition.mountpoint}): {usage.percent}%")
        except:
            log(f'Не удалось получить информацию использования диска {partition}', ERROR)
    return "\n".join(disk_data)
