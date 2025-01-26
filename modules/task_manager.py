import psutil
import ctypes
from .logger import *
from PyQt5.QtGui import QImage, QPixmap

class Process():
    STATUS = {
        psutil.STATUS_RUNNING: "Выполняется",
        psutil.STATUS_SLEEPING: "Спит",
        psutil.STATUS_DISK_SLEEP: "Спит (диск)",
        psutil.STATUS_STOPPED: "Остановлен",
        psutil.STATUS_TRACING_STOP: "Остановлен (трассировка)",
        psutil.STATUS_ZOMBIE: "Зомби",
        psutil.STATUS_DEAD: "Мертв",
        psutil.STATUS_WAKING: "Пробуждается",
        psutil.STATUS_IDLE: "Простаивает",
        psutil.STATUS_LOCKED: "Заблокирован",
        psutil.STATUS_WAITING: "Ожидает",
        psutil.STATUS_LOCKED: "Блокирован",
        psutil.STATUS_PARKED: "Припаркован",
    }
    PROCESS_TYPE = {
        'system': 'Системный',
        'critical': 'Критический',
        'normal': 'Обычный',
    }

    def __init__(self, pid, name, status, cpu_percent, memory_percent, create_time):
        self.process_type = get_process_type(pid)
        self.pid = pid
        self.name = name
        self.status = status
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent
        self.create_time = create_time

    def get_process_icon(self) -> None | QPixmap:
        try:
            if self.pid == 0:
                return None
            # Получение пути к исполняемому файлу процесса
            process = psutil.Process(self.pid)
            exe_path = process.exe()

            # Извлечение иконки из исполняемого файла
            hicon = ctypes.windll.shell32.ExtractIconW(0, exe_path, 0)
            if hicon:
                hdc = ctypes.windll.user32.GetDC(0)
                hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
                hbm = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, 32, 32)
                hbm_old = ctypes.windll.gdi32.SelectObject(hdc_mem, hbm)
                ctypes.windll.user32.DrawIconEx(hdc_mem, 0, 0, hicon, 32, 32, 0, 0, 3)
                ctypes.windll.gdi32.SelectObject(hdc_mem, hbm_old)
                ctypes.windll.gdi32.DeleteDC(hdc_mem)
                ctypes.windll.user32.ReleaseDC(0, hdc)

                # Преобразование Bitmap в QPixmap
                class BITMAP(ctypes.Structure):
                    _fields_ = [
                        ("bmType", ctypes.c_long),
                        ("bmWidth", ctypes.c_long),
                        ("bmHeight", ctypes.c_long),
                        ("bmWidthBytes", ctypes.c_long),
                        ("bmPlanes", ctypes.c_ushort),
                        ("bmBitsPixel", ctypes.c_ushort),
                        ("bmBits", ctypes.c_void_p)
                    ]

                bmpinfo = BITMAP()
                ctypes.windll.gdi32.GetObjectW(hbm, ctypes.sizeof(BITMAP), ctypes.byref(bmpinfo))
                bmpstr = ctypes.create_string_buffer(bmpinfo.bmWidthBytes * bmpinfo.bmHeight)
                ctypes.windll.gdi32.GetBitmapBits(hbm, len(bmpstr), bmpstr)
                image = QImage(bmpstr, bmpinfo.bmWidth, bmpinfo.bmHeight, QImage.Format_ARGB32)
                pixmap = QPixmap.fromImage(image)
                return pixmap
            return None
        except Exception as e:
            log(f"Ошибка при получении иконки процесса с PID {self.pid}: {e}", ERROR)
            return None

    def kill(self):
        """Завершает процесс по PID."""
        try:
            process = psutil.Process(self.pid)
            process.terminate()
            msg = f"Процесс {self.name} ({self.pid}) завершен."
            log(msg)
            return msg
        except Exception as e:
            msg = f"Ошибка завершения процесса {self.name}: {e}"
            log(msg, ERROR)
            return msg

    def suspend(self):
        """
        Приостанавливает процесс с указанным PID.

        :param pid: ID процесса, который нужно приостановить.
        :return: Строка с результатом выполнения операции.
        """
        try:
            process = psutil.Process(self.pid)
            process.suspend()
            msg = f"Процесс с PID {self.pid} успешно приостановлен."
            log(msg)
            return msg
        except psutil.NoSuchProcess:
            msg = f"Ошибка: Процесс с PID {self.pid} не существует."
            log(msg, ERROR)
            return msg
        except psutil.AccessDenied:
            msg = f"Ошибка: Доступ к процессу с PID {self.pid} запрещён."
            log(msg, ERROR)
            return msg
        except Exception as e:
            msg = f"Ошибка при приостановке процесса с PID {self.pid}: {e}"
            log(msg, ERROR)
            return msg

    def resume(self):
        """
        Возобновляет приостановленный процесс с указанным PID.

        :param pid: ID процесса, который нужно возобновить.
        :return: Строка с результатом выполнения операции.
        """
        try:
            process = psutil.Process(self.pid)
            process.resume()
            msg = f"Процесс с PID {self.pid} успешно возобновлён."
            log(msg)
            return msg
        except psutil.NoSuchProcess:
            msg = f"Ошибка: Процесс с PID {self.pid} не существует."
            log(msg, ERROR)
            return msg
        except psutil.AccessDenied:
            msg = f"Ошибка: Доступ к процессу с PID {self.pid} запрещён."
            log(msg, ERROR)
            return msg
        except Exception as e:
            msg = f"Ошибка при возобновлении процесса с PID {self.pid}: {e}"
            log(msg, ERROR)
            return msg


    def __repr__(self):
        return f"Process({self.pid}, {self.name})"
    
    def __str__(self):
        return f"{self.name} ({self.pid})"
    
def get_process_list():
    """Возвращает список активных процессов."""
    processes = []
    for proc in psutil.process_iter(attrs=["pid", "name", "status", "cpu_percent", "memory_percent", "create_time"]):
        processes.append(Process(
            proc.info['pid'],
            proc.info['name'],
            proc.info['status'],
            proc.info['cpu_percent'],
            proc.info['memory_percent'],
            proc.info['create_time']
        ))
    return processes

class ProcessType:
    SYSTEM = 'system'
    CRITICAL = 'critical'
    NORMAL = 'normal'

def get_process_type(pid):
    try:
        if pid == 0:
            return ProcessType.SYSTEM
        process = psutil.Process(pid)
        if process.username() in ['SYSTEM', 'NT AUTHORITY\\SYSTEM', 'NT AUTHORITY\\СИСТЕМА', 'root', 'СИСТЕМА', 'NT AUTHORITY\\LOCAL SERVICE']:
            return ProcessType.SYSTEM # Не стесняйтесь добавлять свои значения!
        elif False: # TODO: Добавить проверку на критические процессы
            return ProcessType.CRITICAL
        else:
            return ProcessType.NORMAL
    except psutil.NoSuchProcess:
        log(f"Процесс с PID {pid} не найден.", WARNING)
        return None
    except Exception as e:
        log(f"Ошибка при определении типа процесса с PID {pid}: {e}", ERROR)
        return None
