#print('Инициализация...')
import ctypes, ctypes.wintypes, os, atexit

WM_CLOSE = 0x0010
WM_SYSCOMMAND = 0x0112
SC_CLOSE = 0xF060
original_wnd_proc = None

current_pid = os.getpid()

def disable_console_close():
    # Получаем handle текущего окна консоли
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd == 0:
        #print("Консольное окно не обнаружено.")
        return
    
    # Получаем текущее меню окна
    hMenu = ctypes.windll.user32.GetSystemMenu(hwnd, False)
    if hMenu == 0:
        #print("Не удалось получить меню системы.")
        return

    # Отключаем пункт "Закрыть"
    SC_CLOSE = 0xF060
    ctypes.windll.user32.RemoveMenu(hMenu, SC_CLOSE, 0x00000000)

    # Обновляем меню консоли
    ctypes.windll.user32.DrawMenuBar(hwnd)
    ##print("Кнопка 'Закрыть' консоли отключена.")

def disable_console_close_by_pid(pid):
    # Ищем консольное окно по PID
    hwnd = None
    def callback(h, _):
        nonlocal hwnd
        process_id = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(h, ctypes.byref(process_id))
        if process_id.value == pid:
            hwnd = h
            return False
        return True

    # Перебираем все окна
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(callback), 0)

    if hwnd:
        # Удаляем кнопку "Закрыть"
        hMenu = ctypes.windll.user32.GetSystemMenu(hwnd, False)
        if hMenu:
            SC_CLOSE = 0xF060
            ctypes.windll.user32.RemoveMenu(hMenu, SC_CLOSE, 0x00000000)
            ctypes.windll.user32.DrawMenuBar(hwnd)
    #        print(f"Кнопка 'Закрыть' отключена для окна с PID {pid}.")
    #    else:
    #        print("Не удалось получить системное меню.")
    #else:
    #    print(f"Окно с PID {pid} не найдено.")

def enable_debug_privileges():
    hToken = ctypes.wintypes.HANDLE()
    TOKEN_ADJUST_PRIVILEGES = 0x0020
    TOKEN_QUERY = 0x0008
    SE_PRIVILEGE_ENABLED = 0x00000002

    class LUID(ctypes.Structure):
        _fields_ = [("LowPart", ctypes.wintypes.DWORD), ("HighPart", ctypes.wintypes.LONG)]

    class TOKEN_PRIVILEGES(ctypes.Structure):
        _fields_ = [("PrivilegeCount", ctypes.wintypes.DWORD),
                    ("Privileges", LUID * 1)]

    luid = LUID()
    if not ctypes.windll.advapi32.LookupPrivilegeValueW(None, "SeDebugPrivilege", ctypes.byref(luid)):
        #print("Ошибка при вызове LookupPrivilegeValueW")
        return False

    if not ctypes.windll.advapi32.OpenProcessToken(
        ctypes.windll.kernel32.GetCurrentProcess(),
        TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
        ctypes.byref(hToken)
    ):
        return False

    tp = TOKEN_PRIVILEGES()
    tp.PrivilegeCount = 1
    tp.Privileges[0].LowPart = luid.LowPart
    tp.Privileges[0].HighPart = luid.HighPart
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED

    ctypes.windll.advapi32.AdjustTokenPrivileges(
        hToken, False, ctypes.byref(tp), ctypes.sizeof(tp), None, None
    )

    if ctypes.windll.kernel32.GetLastError() != 0:
        return False

    return True

def new_wnd_proc(hwnd, msg, wparam, lparam):
    if msg == WM_CLOSE or (msg == WM_SYSCOMMAND and wparam == SC_CLOSE):
        print("Попытка закрыть консоль заблокирована!")
        return 0
    return ctypes.windll.user32.CallWindowProcW(original_wnd_proc, hwnd, msg, wparam, lparam)

def block_console_close():
    global original_wnd_proc

    if not enable_debug_privileges():
        #print("Не удалось включить привилегии SeDebugPrivilege.")
        return

    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd == 0:
        #print("Не удалось получить окно консоли.")
        return

    if ctypes.sizeof(ctypes.c_void_p) == 8:  # 64-битная система
        set_window_long = ctypes.windll.user32.SetWindowLongPtrW
    else:
        set_window_long = ctypes.windll.user32.SetWindowLongW

    original_wnd_proc = set_window_long(
        hwnd, -4, ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.wintypes.HWND, ctypes.wintypes.UINT,
                                     ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)(new_wnd_proc)
    )
    if not original_wnd_proc:
        print("Не удалось установить обработчик оконных сообщений.")
    else:
        print("Закрытие консоли заблокировано.")

    atexit.register(lambda: set_window_long(hwnd, -4, original_wnd_proc))

if __name__ == "__main__":
    block_console_close()
    disable_console_close()
    disable_console_close_by_pid(current_pid)

is_pyi_splash = False

try:
    import pyi_splash
    is_pyi_splash = True
    pyi_splash.update_text("Loading GUI...")
except:
    pass

import sys, traceback
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QPushButton, QCompleter, QLineEdit, QWidget, QMessageBox, qApp, QErrorMessage, QTableView
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWinExtras import QWinTaskbarButton
from modules.system_info import get_system_info, get_disk_info, get_load_info, get_os_icon
from modules.process_launcher import ProcessLauncher
from modules.logger import *
from modules.titles import make_title
from modules.tts import say_async
from ui.antivirus import AntivirusWindow
from ui.disk_manager import DiskManagerWindow
from ui.user_manager import UserManagerWindow
from ui.desktop_manager import DesktopManagerWindow
from ui.system_restore import SystemRestoreWindow
from ui.browser import BrowserWindow
from ui.task_manager import TaskManagerWindow
from ui.software_launcher import SoftwareLauncher
from ui.settings import SettingsWindow
from ui.about import AboutWindow
#from fp.fp import FreeProxy
import qdarktheme
from pyqt_windows_os_light_dark_theme_window.main import Window
import qtawesome
#import qtmdi

#os.system('chcp 65001')

BANNER_TEXT = """
 __   __     _  _       _                 
 \ \ / /___ | || | ___ | | _ __  ___  _ _ 
  \ V // _ \| __ |/ -_)| || '_ \/ -_)| '_|
   |_| \___/|_||_|\___||_|| .__/\___||_|  
                          |_|               
"""

CMD_PROGRAMS_LIST = [
    'regedit',
    'taskmgr',
    'msconfig',
    'tasklist',
    'taskkill',
    'shutdown',
    'systeminfo',
    'ping'
    'sfc',
]

def is_admin():
    """
    Проверяет, запущен ли скрипт с правами администратора.
    :return: True, если скрипт запущен с правами администратора, иначе False.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    """
    Перезапускает скрипт с правами администратора.
    """
    if sys.argv[0] != "main.py":  # Проверка, чтобы избежать бесконечного цикла
        # Запуск скрипта с правами администратора
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def show_error_message(error_message):
    """Показывает окно с сообщением об ошибке."""
    error_dialog = QErrorMessage()
    error_dialog.showMessage(error_message)
    error_dialog.exec_()

class VirusProtectionApp(QMainWindow, Window):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, False)
        self.setWindowTitle(make_title('YoHelper - MultiTool for Windows 10'))
        self.setMinimumSize(900, 400)
        self.resize(1000, 700)
        self.setMaximumSize(1600, 1000)

        self.setStyleSheet("""
* {
    font-size: 16px;
    font-family: 'Consolas';
}
QPushButton {
    padding: 5px 13px;
}
#title {
    font-size: 28px;
    font-weight: bold;
}
""")

        self.software_launcher = SoftwareLauncher(self)

        self.initUI()

        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        self.threads = list()

    def initUI(self):
        # Основной макет
        main_layout = QVBoxLayout()

        premain_layout = QVBoxLayout()

        self.title = QLabel('YoHelper')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet('font-size: 48px;font-weight: bold;font-family: "Comic Sans MS";')
        premain_layout.addWidget(self.title)

        mains_layout = QHBoxLayout()

        side_layout = QVBoxLayout()

        # Система
        system_group = QGroupBox()
        system_group.setTitle("Система")
        system_layout = QVBoxLayout()
        self.system_info_table = QTableView()
        self.system_info_table.setEditTriggers(QTableView.NoEditTriggers)
        self.system_info_table.setSortingEnabled(False)
        self.system_info_table.setShowGrid(False)
        self.system_info_table.verticalHeader().hide()
        self.system_info_table.horizontalHeader().hide()
        system_layout.addWidget(self.system_info_table)
        system_group.setLayout(system_layout)

        # Системная информация
        system_info_group = QGroupBox("Информация")
        system_info_layout = QVBoxLayout()
        self.system_info_label = QLabel("Система: Загрузка...")
        self.disk_info_label = QLabel("Диски: Загрузка...")
        update_system_info_button = QPushButton("Обновить")
        update_system_info_button.clicked.connect(self.update_system_info)
        os_icon = QLabel()
        os_icon.setPixmap(get_os_icon())
        system_info_layout.addWidget(os_icon)
        system_info_layout.addWidget(self.system_info_label)
        system_info_layout.addWidget(self.disk_info_label)
        system_info_layout.addWidget(update_system_info_button)
        system_info_group.setLayout(system_info_layout)
        side_layout.addWidget(system_info_group)

        module_buttons = [
            ("Запуск сторонних программ", self.software_launcher.show, "mdi.apps"),
            ("Антивирус", self.open_antivirus, "mdi.shield-bug"),
            ("Управление дисками", self.open_disk_manager, "mdi.harddisk"),
            ("Управление пользователями", self.open_user_manager, "mdi.account-group"),
            ("Персонализация", self.open_desktop_manager, "mdi.image"),
            ("Точка восстановления", self.open_system_restore, "mdi.restore"),
            ("Браузер", lambda: self.open_browser(), "mdi.web"),
            ("Диспетчер задач", self.open_task_manager, "mdi.apps"),
            ("Выход", qApp.quit, "mdi.exit-to-app"),
        ]

        for text, action, icon in module_buttons:
            btn = QPushButton(text)
            btn.setIcon(qtawesome.icon(icon))
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(action)
            side_layout.addWidget(btn)
            btn.setMinimumHeight(35)

        # Логирование
        log_group = QGroupBox("Логирование")
        log_layout = QVBoxLayout()
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        setup_logger(self.log_text_edit)       
        self.log_text_edit.setHtml(f'<pre style="font-size:8pt;white-space: pre;">{BANNER_TEXT}</pre>')
        self.log_text_edit.setStyleSheet("font-size: 11px;")
        log_layout.addWidget(self.log_text_edit)
        log_group.setLayout(log_layout)

        # Поле запуска команд
        command_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        completer = QCompleter(CMD_PROGRAMS_LIST, self.command_input)
        self.command_input.setCompleter(completer) 
        self.command_input.setPlaceholderText("Введите команду...")
        self.command_input.returnPressed.connect(self.run_command)
        command_run_button = QPushButton("Запустить")
        command_run_button.clicked.connect(self.run_command)
        command_layout.addWidget(self.command_input)
        command_layout.addWidget(command_run_button)

        other_layout = QHBoxLayout()
        other_buttons = [
            ("Настройки", self.open_settings),
            ("Сайт NedoTube", lambda: self.open_browser('https://nedotube.vercel.app/')),
            ("О программе", self.open_about),
        ]

        for text, action in other_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(action)
            other_layout.addWidget(btn)

        # Добавление компонентов в макеты
        mains_layout.addLayout(premain_layout)
        mains_layout.addLayout(side_layout)

        main_layout.addLayout(mains_layout)
        premain_layout.addWidget(system_group)
        premain_layout.addLayout(command_layout)
        premain_layout.addWidget(log_group)
        premain_layout.addLayout(other_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_system_info()

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(1000)

        self.taskbar_button = QWinTaskbarButton(self)
        self.taskbar_button.setWindow(self.windowHandle())
        self.taskbar_button.setOverlayIcon(QIcon(":/loading.png"));
        self.taskbar_progress = self.taskbar_button.progress()
        self.taskbar_progress.setVisible(True)
        self.taskbar_progress.setValue(50)
        self.taskbar_progress.show()

    def on_timer(self):
        self.update_info()

    def update_info(self):
        """Обновляет информацию о системе."""
        self.system_info_label.setText(get_load_info())
        self.disk_info_label.setText(get_disk_info())

    def update_system_info(self):
        system_info = get_system_info()
        model = QStandardItemModel(len(system_info), 2)
        model.setHorizontalHeaderLabels(["Параметр", "Значение"])
        for i, (key, value) in enumerate(system_info.items()):
            model.setItem(i, 0, QStandardItem(key))
            model.setItem(i, 1, QStandardItem(value))
        self.system_info_table.setModel(model)
        self.system_info_table.resizeColumnsToContents()

    def run_command(self):
        """Запускает команду из текстового поля."""
        command = self.command_input.text().strip()
        if not command:
            return
        # запустить в отдельном потоке
        self.command_input.clear()
        self.log_text_edit.append(f"<b>Введена комманда:</b> {command}")

        self.threads.append(QThread()) 
        self.process_launcher = ProcessLauncher(self, command)
        self.process_launcher.setParent(None)
        self.process_launcher.moveToThread(self.threads[-1])
        self.process_launcher.setParent(self)
        self.threads[-1].started.connect(self.process_launcher.launch_process)
        self.threads[-1].start()

    def open_antivirus(self):
        """Открывает окно Антивируса."""
        self.antivirus_window = AntivirusWindow(self)
        self.antivirus_window.show()

    def open_disk_manager(self):
        """Открывает окно Управления дисками."""
        self.disk_manager_window = DiskManagerWindow(self)
        self.disk_manager_window.show()

    def open_user_manager(self):
        """Открывает окно Управления пользователями."""
        self.user_manager_window = UserManagerWindow(self)
        self.user_manager_window.show()

    def open_desktop_manager(self):
        """Открывает окно Управления обоями."""
        self.desktop_manager_window = DesktopManagerWindow(self)
        self.desktop_manager_window.show()

    def open_system_restore(self):
        """Открывает окно Точки восстановления."""
        self.system_restore_window = SystemRestoreWindow(self)
        self.system_restore_window.show()

    def open_browser(self, url = "https://www.google.com/?hl=ru"):
        """Открывает окно Встроенного браузера."""
        self.browser_window = BrowserWindow(self, url)
        self.browser_window.show()

    def open_task_manager(self):
        """Открывает окно Диспетчера задач."""
        self.task_manager_window = TaskManagerWindow(self)
        self.task_manager_window.show()

    def open_settings(self):
        """Открывает окно Настроек."""
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def open_about(self):
        """Открывает окно О программе."""
        self.about_window = AboutWindow(self)
        self.about_window.show()

    #def make_process_critical(self):  # Ненадёжный вариант, т.к. вирусы могут крашнуть систему из-за простого закрытия программы :P
    #    """Устанавливает процесс как критический."""
    #    try:
    #        ntdll = ctypes.WinDLL("ntdll")
    #        hproc = ctypes.windll.kernel32.GetCurrentProcess()
    #        status = ntdll.RtlSetProcessIsCritical(1, 0, 0)
    #        if status != 0:
    #            raise Exception("Не удалось установить процесс как критический.")
    #    except Exception as e:
    #        log(f"Ошибка защиты процесса:\n{str(e)}", ERROR)

    def closeEvent(self, event):
        """Предотвращает закрытие программы."""
        QMessageBox.warning(self, "Предупреждение", "Закрытие программы заблокировано! Используйте кнопку выхода.")
        event.ignore()

from urllib.parse import urlparse

def main():
    def trying_close(**k):
        log('Произошла попытка завершения процесса программы!', WARNING)

    #free_proxy = urlparse(FreeProxy(anonym=True).get())
    #print(free_proxy)
    #proxy = QNetworkProxy()
    #proxy.setType(QNetworkProxy.HttpProxy)
    #proxy.setHostName(free_proxy.hostname)
    #proxy.setPort(free_proxy.port)
    #QNetworkProxy.setApplicationProxy(proxy)

    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    #say_async("Примечание: Чтобы сделать окно поверх всех окон, нажмите сочетание клавиш: Shift + F10")

    QCoreApplication.setQuitLockEnabled(True)  # Включаем блокировку выхода
    window = VirusProtectionApp()
    window.show()
    app.aboutToQuit.connect(trying_close)

    if is_pyi_splash:
        pyi_splash.close()

    sys.exit(app.exec_())

if __name__ == "__main__":
    error_code = ctypes.windll.kernel32.GetLastError()
    if error_code != 0:
        log(f"Ошибка установки обработчика: {error_code}", ERROR)

    if not is_admin():
        print("Попытка запустить с правами администратора...")
        run_as_admin()
    else:
        print('\n\n\n')
        print(BANNER_TEXT)
        try:
            if is_pyi_splash:
                pyi_splash.update_text("Hi!")
            main()
        except Exception as e:
            error_message = traceback.format_exc()
            print(error_message)
            show_error_message(error_message)
            os.system('pause')
