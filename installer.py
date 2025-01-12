import os, shutil, subprocess, sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QRadioButton, QMessageBox,
    QPushButton, QLabel, QWidget, QButtonGroup, QFileDialog, QLineEdit
)
from PyQt5.QtCore import Qt
from modules.titles import make_title
import qdarktheme
from pyqt_windows_os_light_dark_theme_window.main import Window

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    
main_exe = "NedoHelper.exe"  # Имя файла программы

class InstallerWindow(Window):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title("Установщик программы"))
        self.setFixedSize(500, 250)

        # Основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Макет
        layout = QVBoxLayout(central_widget)

        # Большой текст сверху
        self.header_label = QLabel("Добро пожаловать в установщик программы!")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.header_label)

        # Радио-кнопки
        self.prepare_system_radio = QRadioButton("Установить программу и подготовить систему")
        self.open_program_radio = QRadioButton("Просто открыть программу")
        self.open_program_radio.setChecked(True)  # Установить выбранным по умолчанию

        # Группа для радио-кнопок (опционально)
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.prepare_system_radio)
        self.radio_group.addButton(self.open_program_radio)

        layout.addWidget(self.prepare_system_radio)
        layout.addWidget(self.open_program_radio)

        # Поле для отображения выбранного пути
        self.path_label = QLabel("Путь установки:")
        self.path_label.setVisible(False)
        layout.addWidget(self.path_label)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Выберите папку установки")
        self.path_input.setReadOnly(True)
        self.path_input.setVisible(False)
        layout.addWidget(self.path_input)

        # Кнопка выбора пути
        self.browse_button = QPushButton("Обзор")
        self.browse_button.setVisible(False)
        self.browse_button.clicked.connect(self.select_install_path)
        layout.addWidget(self.browse_button)

        # Большая кнопка снизу
        self.install_button = QPushButton("Установить")
        self.install_button.setFixedHeight(40)
        self.install_button.clicked.connect(self.on_install_button_clicked)
        layout.addWidget(self.install_button)

        # Связывание радио-кнопок с обновлением текста на кнопке
        self.prepare_system_radio.toggled.connect(self.update_ui_elements)

        # Путь установки
        self.install_path = ""

    def update_ui_elements(self):
        """
        Обновляет текст на кнопке и элементы интерфейса в зависимости от выбора радио-кнопки.
        """
        if self.prepare_system_radio.isChecked():
            self.install_button.setText("Установить")
            self.path_label.setVisible(True)
            self.path_input.setVisible(True)
            self.browse_button.setVisible(True)
        else:
            self.install_button.setText("Открыть")
            self.path_label.setVisible(False)
            self.path_input.setVisible(False)
            self.browse_button.setVisible(False)

    def select_install_path(self):
        """
        Открывает диалог выбора папки для установки.
        """
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку установки")
        if folder:
            self.install_path = folder
            self.path_input.setText(folder)

    def on_install_button_clicked(self):
        """
        Обработчик нажатия на кнопку.
        Выполняет действия в зависимости от выбора.
        """
        if self.prepare_system_radio.isChecked():
            if not self.install_path:
                QMessageBox.warning(self, "Внимание!", "Выберите папку перед установкой!")
                return
            self.prepare_system()
        else:
            self.open_program()

    def prepare_system(self):
        """
        Логика подготовки системы: копирование main.exe в указанную папку.
        """
        if not os.path.isfile(main_exe):
            QMessageBox.critical(self, "Ошибка!", "Программа не найдена!")
            return

        try:
            # Создаем папку, если ее нет
            os.makedirs(self.install_path, exist_ok=True)

            # Копируем файл main.exe
            target_path = os.path.join(self.install_path, main_exe)
            shutil.copy(os.path.join(application_path, main_exe), target_path)

            # Подтверждение успешной установки
            QMessageBox.information(self, "Установка завершена!", f"Программа установлена в: {self.install_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка установки!", f"{e}")

    def open_program(self):
        """
        Логика запуска программы.
        """
        try:
            subprocess.Popen(os.path.join(application_path, main_exe))
        except:
            QMessageBox.critical(self, "Ошибка запуска!", "Не удалось запустить программу! Попробуйте установить его.")



if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    installer = InstallerWindow()
    installer.show()

    sys.exit(app.exec_())
