import sys, os, ctypes, traceback, signal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from modules.system_info import get_system_info, get_disk_info
from modules.process_launcher import launch_process
from modules.logger import *
from modules.titles import make_title
from ui.antivirus import AntivirusWindow
from ui.disk_manager import DiskManagerWindow
from ui.user_manager import UserManagerWindow
from ui.desktop_manager import DesktopManagerWindow
from ui.system_restore import SystemRestoreWindow
from ui.browser import BrowserWindow
from ui.task_manager import TaskManagerWindow
from ui.software_launcher import SoftwareLauncher

os.system('chcp 65001')

BANNER_TEXT = """::::    ::: :::::::::: :::::::::   ::::::::  :::    ::: :::::::::: :::        :::::::::  :::::::::: :::::::::  
:+:+:   :+: :+:        :+:    :+: :+:    :+: :+:    :+: :+:        :+:        :+:    :+: :+:        :+:    :+: 
:+:+:+  +:+ +:+        +:+    +:+ +:+    +:+ +:+    +:+ +:+        +:+        +:+    +:+ +:+        +:+    +:+ 
+#+ +:+ +#+ +#++:++#   +#+    +:+ +#+    +:+ +#++:++#++ +#++:++#   +#+        +#++:++#+  +#++:++#   +#++:++#:  
+#+  +#+#+# +#+        +#+    +#+ +#+    +#+ +#+    +#+ +#+        +#+        +#+        +#+        +#+    +#+ 
#+#   #+#+# #+#        #+#    #+# #+#    #+# #+#    #+# #+#        #+#        #+#        #+#        #+#    #+# 
###    #### ########## #########   ########  ###    ### ########## ########## ###        ########## ###    ### 
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

class VirusProtectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title('NedoHelper - MultiTool for Windows 10'))
        self.setMaximumSize(1000, 700)

        self.initUI()

    def initUI(self):
        # Основной макет
        main_layout = QVBoxLayout()

        premain_layout = QVBoxLayout()

        mains_layout = QHBoxLayout()

        # Верхняя панель кнопок
        button_layout = QHBoxLayout()

        side_layout = QVBoxLayout()

        module_buttons = [
            ("Антивирус", self.open_antivirus),
            ("Управление дисками", self.open_disk_manager),
            ("Управление пользователями", self.open_user_manager),
            ("Смена обоев", self.open_desktop_manager),
            ("Точка восстановления", self.open_system_restore),
            ("Браузер", self.open_browser),
            ("Диспетчер задач", self.open_task_manager),
            ("Выход", qApp.quit),
        ]

        for text, action in module_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(action)
            button_layout.addWidget(btn)

        # Системная информация
        system_info_group = QGroupBox("Системная информация")
        system_info_layout = QVBoxLayout()
        self.system_info_label = QLabel("Система: Загрузка...")
        self.disk_info_label = QLabel("Диски: Загрузка...")
        system_info_layout.addWidget(self.system_info_label)
        system_info_layout.addWidget(self.disk_info_label)
        system_info_group.setLayout(system_info_layout)

        # Логирование
        log_group = QGroupBox("Логирование")
        log_layout = QVBoxLayout()
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        setup_logger(self.log_text_edit)       
        self.log_text_edit.setHtml(f'<pre style="font-size:7pt;white-space: pre;">{BANNER_TEXT}</pre>')
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

        # Система
        system_group = QGroupBox()
        side_layout.addWidget(system_group)

        # Добавление компонентов в макеты
        mains_layout.addLayout(premain_layout)
        mains_layout.addLayout(side_layout)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(mains_layout)
        premain_layout.addWidget(system_info_group)
        premain_layout.addLayout(command_layout)
        premain_layout.addWidget(log_group)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_system_info()

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(1000)

    def on_timer(self):
        self.update_system_info()

    def update_system_info(self):
        """Обновляет информацию о системе."""
        system_info = get_system_info()
        disk_info = get_disk_info()
        self.system_info_label.setText(system_info)
        self.disk_info_label.setText(disk_info)

    def run_command(self):
        """Запускает команду из текстового поля."""
        command = self.command_input.text().strip()
        if not command:
            return
        result = launch_process(command, admin=True)
        log(result, INFO)

    def open_antivirus(self):
        """Открывает окно Антивируса."""
        self.antivirus_window = AntivirusWindow()
        self.antivirus_window.show()

    def open_disk_manager(self):
        """Открывает окно Управления дисками."""
        self.disk_manager_window = DiskManagerWindow()
        self.disk_manager_window.show()

    def open_user_manager(self):
        """Открывает окно Управления пользователями."""
        self.user_manager_window = UserManagerWindow()
        self.user_manager_window.show()

    def open_desktop_manager(self):
        """Открывает окно Управления обоями."""
        self.desktop_manager_window = DesktopManagerWindow()
        self.desktop_manager_window.show()

    def open_system_restore(self):
        """Открывает окно Точки восстановления."""
        self.system_restore_window = SystemRestoreWindow()
        self.system_restore_window.show()

    def open_browser(self):
        """Открывает окно Встроенного браузера."""
        self.browser_window = BrowserWindow()
        self.browser_window.show()

    def open_task_manager(self):
        """Открывает окно Диспетчера задач."""
        self.task_manager_window = TaskManagerWindow()
        self.task_manager_window.show()

    def open_software_launcher(self):
        """Открывает окно Запуска стороних программ."""
        self.software_launcher = SoftwareLauncher()
        self.software_launcher.show()

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

def main():
    app = QApplication(sys.argv)
    window = VirusProtectionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":

    # Запрещаем завершение текущего процесса
    kernel32 = ctypes.windll.kernel32
    PROCESS_TERMINATE = 0x0001
    # Отключаем права на завершение для текущего процесса
    handle = kernel32.OpenProcess(PROCESS_TERMINATE, False, os.getpid())
    kernel32.SetHandleInformation(handle, PROCESS_TERMINATE, 0)
    kernel32.SetConsoleCtrlHandler(None, True)

    # Функция обработчик сигналов
    def trying_close(**k):
        log('Произошла попытка завершения процесса программы!', WARNING)

    # Игнорирование сигналов
    signal.signal(signal.SIGINT, trying_close)  # Игнорировать Ctrl+C
    signal.signal(signal.SIGTERM, trying_close)  # Игнорировать kill
    

    if not is_admin():
        print("Попытка запустить с правами администратора...")
        run_as_admin()
    else:
        print(BANNER_TEXT)
        try:
            main()
        except Exception as e:
            print(traceback.format_exc())
            os.system('pause')
