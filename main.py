import sys, os, ctypes, subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QTextEdit, QLineEdit, QGroupBox
)
from PyQt5.QtCore import Qt
from system_info import get_system_info, get_disk_info
from process_launcher import launch_process
from logger import log
from antivirus_ui import AntivirusWindow
from disk_manager_ui import DiskManagerWindow
from user_manager_ui import UserManagerWindow
from desktop_manager_ui import DesktopManagerWindow
from system_restore_ui import SystemRestoreWindow
from browser_ui import BrowserWindow
from task_manager_ui import TaskManagerWindow

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
        self.setWindowTitle("System Helper")
        self.setFixedSize(1000, 700)

        self.initUI()

    def initUI(self):
        # Основной макет
        main_layout = QVBoxLayout()

        # Верхняя панель кнопок
        button_layout = QHBoxLayout()

        module_buttons = [
            ("Антивирус", self.open_antivirus),
            ("Управление дисками", self.open_disk_manager),
            ("Управление пользователями", self.open_user_manager),
            ("Смена обоев", self.open_desktop_manager),
            ("Точка восстановления", self.open_system_restore),
            ("Встроенный браузер", self.open_browser),
            ("Диспетчер задач", self.open_task_manager),
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
        log_layout.addWidget(self.log_text_edit)
        log_group.setLayout(log_layout)

        # Поле запуска команд
        command_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Введите команду...")
        self.command_input.returnPressed.connect(self.run_command)
        command_run_button = QPushButton("Запустить")
        command_run_button.clicked.connect(self.run_command)
        command_layout.addWidget(self.command_input)
        command_layout.addWidget(command_run_button)

        # Добавление компонентов в основной макет
        main_layout.addLayout(button_layout)
        main_layout.addWidget(system_info_group)
        main_layout.addWidget(log_group)
        main_layout.addLayout(command_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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
        log(result, level="info")
        self.log_text_edit.append(result)

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


def main():
    app = QApplication(sys.argv)
    window = VirusProtectionApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if not is_admin():
        print("Попытка запустить с правами администратора...")
        run_as_admin()
    else:
        print('Ура!')
        main()
