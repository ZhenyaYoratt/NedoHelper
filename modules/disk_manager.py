import ctypes
import win32com.client
from ctypes import wintypes

import psutil
import os

from .logger import *
from PyQt5.QtGui import QPixmap, QImage

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
        msg = f"Ошибка определения типа диска: {e}"
        log(msg, ERROR)
        return msg

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
        log(f"Ошибка при проверке статуса диска {drive_letter}: {e}", ERROR)
        return False

class DriveInfo:
    def __init__(self, status = False, letter = None, type = None):
        self.status = False
        self.letter = None
        self.type = None

def get_drive_info(drive_letter):
    """
    Получает информацию о диске: тип и доступность.
    
    :param drive_letter: Буква диска, например, "C:".
    :return: Строка с информацией о типе и статусе устройства.
    """
    if check_disk_status(drive_letter):
        disk_type = get_disk_type(drive_letter)
        return DriveInfo(status=True, letter=drive_letter, type=disk_type)
    else:
        return DriveInfo(status=False, letter=drive_letter)

def unlock_bitlocker(drive_letter):
    """Попытка разблокировать диск с BitLocker."""
    try:
        result = ctypes.windll.kernel32.BitLockerUnlock(drive_letter)
        if result:
            return f"Диск {drive_letter} разблокирован."
        return f"Не удалось разблокировать диск {drive_letter}."
    except Exception as e:
        msg = f"Ошибка разблокировки диска: {e}"
        log(msg, ERROR)
        return msg

def is_bitlocker_protected(drive_letter):
    """
    Проверяет, защищен ли диск BitLocker.
    
    :param drive_letter: Буква диска, например, 'C:'.
    :return: True, если диск защищен BitLocker, иначе False.
    """
    try:
        # Подключение к WMI
        wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\CIMV2\\Security\\MicrosoftVolumeEncryption")
        
        letter = drive_letter.replace('/', '').replace('\\', '')

        # Запрос состояния шифрования для всех дисков
        query = f'SELECT * FROM Win32_EncryptableVolume WHERE DeviceID="{letter}"'
        volumes = wmi.ExecQuery(query)
        
        for volume in volumes:
            # Состояние шифрования:
            # 0 - Нет шифрования, 1 - Шифрование включено
            if volume.ProtectionStatus == 1:
                return True
        return False
    except Exception as e:
        log(f"Ошибка проверки защиты BitLocker: {e}", ERROR)
        return None

def get_volume_name(drive_letter: str):
    try:
        # Подключение к WMI
        wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
        
        letter = drive_letter.replace('/', '').replace('\\', '')

        # Запрос имени тома для указанного диска
        query = f'SELECT * FROM Win32_LogicalDisk WHERE DeviceID="{letter}"'
        volumes = wmi.ExecQuery(query)

        for volume in volumes:
            return volume.VolumeName
        return None
    except Exception as e:
        log(f"Ошибка получения имени тома диска: {e}", ERROR)
        return None

import win32ui
import win32gui

# Определение структуры BITMAP
class BITMAP(ctypes.Structure):
    _fields_ = [
        ("bmType", wintypes.LONG),
        ("bmWidth", wintypes.LONG),
        ("bmHeight", wintypes.LONG),
        ("bmWidthBytes", wintypes.LONG),
        ("bmPlanes", wintypes.WORD),
        ("bmBitsPixel", wintypes.WORD),
        ("bmBits", ctypes.c_void_p),
    ]

# Определение структуры ICONINFO
class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", wintypes.BOOL),
        ("xHotspot", wintypes.DWORD),
        ("yHotspot", wintypes.DWORD),
        ("hbmMask", wintypes.HBITMAP),
        ("hbmColor", wintypes.HBITMAP),
    ]

def iconToQImage(hIcon):
    # Получаем информацию об иконке
    icon_info = ICONINFO()
    if not ctypes.windll.user32.GetIconInfo(hIcon, ctypes.byref(icon_info)):
        raise ctypes.WinError()

    # Получаем размеры иконки
    bmp_info = BITMAP()
    ctypes.windll.gdi32.GetObjectW(icon_info.hbmColor, ctypes.sizeof(BITMAP), ctypes.byref(bmp_info))

    width = bmp_info.bmWidth
    height = bmp_info.bmHeight

    hdc = win32gui.GetDC(0)
    hdc_mem = win32gui.CreateCompatibleDC(hdc)
    hbmp = win32gui.CreateCompatibleBitmap(hdc, width, height)
    win32gui.SelectObject(hdc_mem, hbmp)

    win32gui.DrawIconEx(hdc_mem, 0, 0, hIcon, width, height, 0, None, 0x0003)

    bmp_str = win32gui.GetBitmapBits(hbmp, True)

    image = QImage(bmp_str, width, height, QImage.Format_ARGB32)

    win32gui.DeleteObject(hbmp)
    win32gui.DeleteDC(hdc_mem)
    win32gui.ReleaseDC(0, hdc)

    return image

def get_disk_icon(drive_letter):
    SHGFI_ICON = 0x000000100
    SHGFI_LARGEICON = 0x000000000
    SHGFI_USEFILEATTRIBUTES = 0x000000010

    class SHFILEINFO(ctypes.Structure):
        _fields_ = [
            ("hIcon", ctypes.c_void_p),
            ("iIcon", ctypes.c_int),
            ("dwAttributes", ctypes.c_ulong),
            ("szDisplayName", ctypes.c_wchar * 260),
            ("szTypeName", ctypes.c_wchar * 80),
        ]

    shfileinfo = SHFILEINFO()
    ctypes.windll.shell32.SHGetFileInfoW(
        f"{drive_letter}",
        0,
        ctypes.byref(shfileinfo),
        ctypes.sizeof(shfileinfo),
        SHGFI_ICON | SHGFI_LARGEICON | SHGFI_USEFILEATTRIBUTES,
    )

    hIcon = shfileinfo.hIcon
    if hIcon:
        # Конвертация иконки в QPixmap
        image = iconToQImage(hIcon)
        icon = QPixmap.fromImage(image)
        ctypes.windll.user32.DestroyIcon(hIcon)
        return icon
    else:
        return None
