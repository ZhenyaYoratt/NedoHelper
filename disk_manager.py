import ctypes
import win32com.client

import psutil
import os

def get_disk_type(drive_letter):
    """
    Получает тип устройства для указанного диска.
    
    :param drive_letter: Буква диска, например, "C:" или "D:".
    :return: Строка с типом устройства (например, "Физический диск", "CD-ROM", "USB", и т.д.)
    """
    try:
        # Проверяем доступность диска
        if not os.path.exists(drive_letter):
            return f"{drive_letter} не доступен."

        # Получаем информацию о разделе диска
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if partition.device.startswith(drive_letter):
                # Определяем тип устройства (например, физический диск или CD-ROM)
                if 'cdrom' in partition.opts:
                    return "CD-ROM"
                elif 'usb' in partition.opts:
                    return "USB"
                else:
                    return "Физический диск"
        return "Неизвестный тип устройства"
    except Exception as e:
        return f"Ошибка определения типа диска: {e}"

def check_disk_status(drive_letter):
    """
    Проверяет, готов ли диск к использованию (например, доступен ли он для чтения).
    
    :param drive_letter: Буква диска (например, "C:", "D:").
    :return: Статус доступности диска (True - доступен, False - не доступен).
    """
    try:
        # Проверяем доступность устройства
        return os.path.exists(drive_letter) and os.access(drive_letter, os.R_OK)
    except Exception as e:
        print(f"Ошибка при проверке статуса диска {drive_letter}: {e}")
        return False

def get_drive_info(drive_letter):
    """
    Получает информацию о диске: тип и доступность.
    
    :param drive_letter: Буква диска, например, "C:".
    :return: Строка с информацией о типе и статусе устройства.
    """
    if check_disk_status(drive_letter):
        disk_type = get_disk_type(drive_letter)
        return f"{drive_letter} доступен. Тип устройства: {disk_type}"
    else:
        return f"{drive_letter} не доступен."

def unlock_bitlocker(drive_letter):
    """Попытка разблокировать диск с BitLocker."""
    try:
        result = ctypes.windll.kernel32.BitLockerUnlock(drive_letter)
        if result:
            return f"Диск {drive_letter} разблокирован."
        return f"Не удалось разблокировать диск {drive_letter}."
    except Exception as e:
        return f"Ошибка разблокировки диска: {e}"

def is_bitlocker_protected(drive_letter):
    """
    Проверяет, защищен ли диск BitLocker.
    
    :param drive_letter: Буква диска, например, 'C:'.
    :return: True, если диск защищен BitLocker, иначе False.
    """
    try:
        # Подключение к WMI
        wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\CIMV2\\Security\\MicrosoftVolumeEncryption")
        
        # Запрос состояния шифрования для всех дисков
        query = f"SELECT * FROM Win32_EncryptableVolume WHERE DriveLetter = '{drive_letter}'"
        volumes = wmi.ExecQuery(query)
        
        for volume in volumes:
            # Состояние шифрования:
            # 0 - Нет шифрования, 1 - Шифрование включено
            if volume.ProtectionStatus == 1:
                return True
        return False
    except Exception as e:
        print(f"Ошибка проверки защиты BitLocker: {e}")
        return False
