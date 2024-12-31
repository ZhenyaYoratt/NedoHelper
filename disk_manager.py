import ctypes
import win32com.client

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
