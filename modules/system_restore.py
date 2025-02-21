from .logger import *
from subprocess import CalledProcessError, run
from wmi import WMI

class RestorePoint:
    def __init__(self, sequence_number, description, creation_time):
        self.sequence_number = sequence_number
        self.description = description
        self.creation_time = creation_time

def list_restore_points():
    try:
        c = WMI()
        points = list()
        for rp in c.Win32_RestorePoint():
            points.append(RestorePoint(rp.SequenceNumber, rp.Description, rp.CreationTime))
    except Exception as e:
        log(f"Error listing restore points: {e}", ERROR)
        return []

def create_restore_point(description="Custom Restore Point", restore_type=0, event_type=100):
    """
    Создаёт точку восстановления системы с указанным описанием.

    :param description: Описание точки восстановления.
    :return: Результат операции (True/False).
    """
    try:
        c = WMI()
        sr = c.Win32_SystemRestore()
        result = sr.CreateRestorePoint(description, restore_type, event_type)
        if result == 0:
            log(f"Точка восстановления создана: {description}")
        else:
            log("Ошибка создания точки восстановления.", ERROR)
        return result
    except Exception as e:
        log("Ошибка создания точки восстановления: " + str(e), ERROR)
        return False

def delete_restore_point(sequence_number):
    try:
        c = WMI()
        for rp in c.Win32_RestorePoint():
            if rp.SequenceNumber == sequence_number:
                rp.Delete()
                print(f"Restore point {sequence_number} deleted.")
                return True
        print("Restore point not found.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def restore_to_point(sequence_number):
    """
    Выполняет восстановление системы до указанной точки восстановления.

    :param sequence_number: Номер последовательности точки восстановления.
    :return: Результат операции (True/False).
    """
    try:
        c = WMI()
        sr = c.Win32_SystemRestore()
        result = sr.Restore(sequence_number)
        if result == 0:
            log(f"Система восстановлена до точки {sequence_number}.")
        else:
            log(f"Ошибка восстановления до точки {result}", ERROR)
        return result
    except Exception as e:
        log(f"Ошибка восстановления до точки {sequence_number}: {e}", ERROR)
        return False

def enable_system_protection():
    try:
        run(["wmic", "/Namespace:\\root\\default", "Path", "SystemRestore", "Call", "Enable", "C:\\"], check=True)
        print("System protection enabled on C:\\")
    except CalledProcessError as e:
        log(f"Error enabling system protection: {e}", ERROR)
        return False

def disable_system_protection():
    try:
        run(["wmic", "/Namespace:\\root\\default", "Path", "SystemRestore", "Call", "Disable", "C:\\"], check=True)
        print("System protection disabled on C:\\")
    except CalledProcessError as e:
        log(f"Error disabling system protection: {e}", ERROR)
        return False

def is_system_protection_enabled():
    try:
        result = run(["wmic", "/Namespace:\\root\\default", "Path", "SystemRestore", "Get", "Enable"], capture_output=True, text=True)
        return "TRUE" in result.stdout.upper()
    except CalledProcessError as e:
        log(f"Error checking system protection status: {e}", ERROR)
        return False
    
def toggle_system_protection():
    if is_system_protection_enabled():
        disable_system_protection()
    else:
        enable_system_protection()