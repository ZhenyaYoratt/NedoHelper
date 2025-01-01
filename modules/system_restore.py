import ctypes
from ctypes.wintypes import DWORD, BOOL, LPCWSTR
from .logger import *

# Загрузка библиотеки SRClient.dll для работы с точками восстановления
srclient = ctypes.WinDLL("Srclient.dll")

# Константы
SR_TYPE_APPLICATION_INSTALL = 0  # Тип точки восстановления - установка приложения
SR_TYPE_APPLICATION_UNINSTALL = 1  # Удаление приложения
SR_TYPE_DEVICE_DRIVER_INSTALL = 10  # Установка драйвера
SR_TYPE_MODIFY_SETTINGS = 12  # Изменение настроек
SR_TYPE_CANCELLED_OPERATION = 13  # Отменённая операция

# Прототипы функций
CreateRestorePointW = srclient.SRSetRestorePointW
CreateRestorePointW.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(DWORD)]
CreateRestorePointW.restype = BOOL


class RESTORE_POINT_INFO(ctypes.Structure):
    _fields_ = [
        ("dwEventType", DWORD),
        ("dwRestorePtType", DWORD),
        ("llSequenceNumber", ctypes.c_longlong),
        ("szDescription", LPCWSTR),
    ]


class STATEMGR_STATUS(ctypes.Structure):
    _fields_ = [
        ("nStatus", DWORD),
        ("llSequenceNumber", ctypes.c_longlong),
    ]


def create_restore_point(description="Custom Restore Point"):
    """
    Создаёт точку восстановления системы с указанным описанием.

    :param description: Описание точки восстановления.
    :return: Результат операции (True/False).
    """
    restore_point_info = RESTORE_POINT_INFO()
    restore_point_info.dwEventType = 100  # Начало создания точки восстановления
    restore_point_info.dwRestorePtType = SR_TYPE_MODIFY_SETTINGS
    restore_point_info.llSequenceNumber = 0
    restore_point_info.szDescription = description

    status = STATEMGR_STATUS()
    result = CreateRestorePointW(ctypes.byref(restore_point_info), ctypes.byref(status))

    if result:
        log(f"Точка восстановления создана: {description}")
    else:
        log("Ошибка создания точки восстановления.", ERROR)

    return result


def restore_to_point(sequence_number):
    """
    Выполняет восстановление системы до указанной точки восстановления.

    :param sequence_number: Номер последовательности точки восстановления.
    :return: Результат операции (True/False).
    """
    try:
        # Восстановление выполняется через команду Windows
        import subprocess

        command = f"rstrui.exe /restore {sequence_number}"
        subprocess.run(command, check=True, shell=True)
        log(f"Система восстановлена до точки {sequence_number}.")
        return True
    except Exception as e:
        log(f"Ошибка восстановления до точки {sequence_number}: {e}", ERROR)
        return False
