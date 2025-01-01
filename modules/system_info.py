import psutil
from .logger import *
from .disk_manager import check_disk_status, get_disk_type

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
            if check_disk_status(partition.mountpoint):
                usage = psutil.disk_usage(partition.mountpoint)
                disk_data.append(f"[{get_disk_type(partition.mountpoint)}] {partition.mountpoint}: занято {usage.percent}%")
            else:
                disk_data.append(f"[{get_disk_type(partition.mountpoint)}] {partition.mountpoint}: недоступен")
        except:
            log(f'Не удалось получить информацию использования диска {partition}', WARN)
    return "\n".join(disk_data)
