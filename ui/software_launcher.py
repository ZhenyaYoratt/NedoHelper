import os
import requests
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt

# Ссылки для загрузки программ
SOFTWARE_URLS = {
    "ProcessHacker": "https://raw.githubusercontent.com/ZhenyaYoratt/NedoHelper/refs/heads/main/software/processhacker-2.39-bin.zip",
    "AnVir Task Manager": "https://www.anvir.com/downloads/taskfree.zip",
    "Autoruns": "https://download.sysinternals.com/files/Autoruns.zip",
    "SimpleUnlocker": "https://simpleunlocker.ds1nc.ru/release/simpleunlocker_release-u.zip",
    "RegCool": "https://kurtzimmermann.com/files/RegCoolX64.zip",
    "RegAlyzer": "https://2ioa6q.soft-load.eu/b4/7/0/660d78274ab175953ccfa5f2f0d43a4c/regalyz-1.6.2.16.exe",
    "Total Commander": "https://totalcommander.ch/1103/tcmd1103x32_64.exe",
}

# Локальная папка для программ
SOFTWARE_DIR = "software"

class SoftwareLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Запуск сторонних программ")
        self.setFixedSize(400, 300)

        # Основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Макет
        layout = QVBoxLayout(central_widget)

        # Заголовок
        header_label = QLabel("Выберите программу для запуска:")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header_label)

        # Кнопки для запуска программ
        for program_name in SOFTWARE_URLS.keys():
            button = QPushButton(program_name)
            button.clicked.connect(lambda checked, p=program_name: self.launch_program(p))
            layout.addWidget(button)

    def launch_program(self, program_name):
        """
        Проверяет наличие программы, загружает при необходимости и запускает.
        """
        # Формируем путь к исполняемому файлу
        program_path = os.path.join(SOFTWARE_DIR, program_name)

        # Проверяем наличие программы
        if not os.path.exists(program_path):
            reply = QMessageBox.question(
                self,
                "Программа отсутствует",
                f"Программа {program_name} отсутствует. Хотите загрузить ее?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.download_program(program_name)
            else:
                return

        # Пытаемся запустить программу
        try:
            subprocess.Popen(program_path, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить программу {program_name}.\n{e}")

    def download_program(self, program_name):
        """
        Загружает программу из интернета в папку software.
        """
        url = SOFTWARE_URLS.get(program_name)
        if not url:
            QMessageBox.critical(self, "Ошибка", f"Ссылка для загрузки {program_name} отсутствует.")
            return

        try:
            # Убедимся, что папка software существует
            os.makedirs(SOFTWARE_DIR, exist_ok=True)

            # Путь для сохранения файла
            file_path = os.path.join(SOFTWARE_DIR, os.path.basename(url))

            # Загрузка файла
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            QMessageBox.information(self, "Успех", f"Программа {program_name} успешно загружена.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить {program_name}.\n{e}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    launcher = SoftwareLauncher()
    launcher.show()
    sys.exit(app.exec_())
