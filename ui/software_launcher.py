import os
import requests
import subprocess
import zipfile
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QMessageBox, QProgressBar
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QUrl

# Ссылки для загрузки программ
SOFTWARE_URLS = {
    "ProcessHacker": {
        "url": "https://raw.githubusercontent.com/ZhenyaYoratt/NedoHelper/refs/heads/main/hosted_softwares/processhacker-2.39-bin.zip",
        "path": "/x64/ProcessHacker.exe",
    },
    "AnVir Task Manager": {
        "url": "https://www.anvir.net/downloads/anvirrus.zip",
        "path": "AnVir.exe",
        "zip": "anvirrus-portable.zip"
    },
    "Autoruns": {
        "url": "https://download.sysinternals.com/files/Autoruns.zip",
        "path": "Autoruns.exe",
    },
    "SimpleUnlocker": {
        "url": "https://mirror.ds1nc.ru/su/release/simpleunlocker_release.zip",
        "path": "simpleunlocker_release/SU.exe",
    },
    "SimpleUnlocker (c утилитами)": {
        "url": "https://mirror.ds1nc.ru/su/release/simpleunlocker_release-u.zip",
        "path": "simpleunlocker_release/SU.exe",
    },
    "RegCool": {
        "url": "https://kurtzimmermann.com/files/RegCoolX64.zip",
        "path": "RegCool.exe",
    },
    "RegAlyzer": {
        "url": "https://download2.portableapps.com/portableapps/RegAlyzerPortable/RegAlyzerPortable_1.6.2.16.paf.exe",
    },
    "Total Commander": {
        "url": "https://totalcommander.ch/1103/tcmd1103x32_64.exe",
    },
    "CCleaner": {
        "url": "https://download.ccleaner.com/portable/ccsetup631.zip",
        "path": "CCleaner.exe",
    },
}

SOFTWARE_DIR = "software"

class DownloadSoftwareWorker(QObject):
    progress = pyqtSignal(int)  # Для прогресса
    completed = pyqtSignal(str)  # Для завершения
    error = pyqtSignal(str)  # Для ошибок
    set_max = pyqtSignal(int)

    def __init__(self, parent, url, save_path):
        super().__init__()
        self.setParent(parent)
        self.url = url
        self.save_path = save_path
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.on_finished)

    def run(self):
        request = QNetworkRequest(QUrl(self.url))
        self.reply = self.manager.get(request)
        self.reply.downloadProgress.connect(self.on_download_progress)

    def on_download_progress(self, bytes_received, bytes_total):
        if bytes_total > 0:
            self.set_max.emit(bytes_total)
            self.progress.emit(bytes_received)

    def on_finished(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            with open(self.save_path, "wb") as file:
                file.write(reply.readAll())
            self.completed.emit(self.save_path)
        else:
            self.error.emit(str(reply.errorString()))
        reply.deleteLater()

class SoftwareLauncher(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle("Запуск сторонних программ")
        self.setMinimumSize(400, 250)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        # Основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Макет
        layout = QVBoxLayout(central_widget)

        # Заголовок
        header_label = QLabel("Выберите программу для запуска:")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setObjectName("title")
        layout.addWidget(header_label)

        # Кнопки для запуска программ
        for program_name in SOFTWARE_URLS.keys():
            button = QPushButton(program_name)
            button.clicked.connect(lambda checked, p=program_name: self.launch_program(p))
            layout.addWidget(button)

    def launch_program(self, program_name):
        program = SOFTWARE_URLS.get(program_name)
        program_path = os.path.abspath(os.path.join(SOFTWARE_DIR, os.path.basename(program['url'])))

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
                return
            else:
                return

        # Запускаем программу
        try:
            if program_path.endswith(".zip"):
                os.startfile(os.path.abspath(os.path.join(SOFTWARE_DIR, os.path.basename(program['url']).replace('.zip', ''), program['path'])))
            else:
                os.startfile(program_path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить программу {program_name}.\n{e}")

    def download_program(self, program_name):
        program = SOFTWARE_URLS.get(program_name)

        if not program:
            QMessageBox.critical(self, "Ошибка", f"Ссылка для загрузки {program_name} отсутствует.")
            return

        os.makedirs(SOFTWARE_DIR, exist_ok=True)
        file_path = os.path.join(SOFTWARE_DIR, os.path.basename(program['url']))

        # Настраиваем поток
        progress_bar = QProgressBar()
        self.centralWidget().layout().addWidget(progress_bar)
        progress_bar.setValue(0)

        self.worker = DownloadSoftwareWorker(self, program['url'], file_path)
        self.worker.set_max.connect(progress_bar.setMaximum)
        self.worker.progress.connect(progress_bar.setValue)
        self.worker.completed.connect(lambda path: self.on_download_completed(path, program_name, program, progress_bar))
        self.worker.error.connect(lambda error: self.on_download_error(error, progress_bar))
        thread = QThread(self.parent())
        self.worker.moveToThread(thread)
        thread.started.connect(self.worker.run)
        thread.start()

    def on_download_completed(self, file_path, program_name, program, progress_bar: QProgressBar):
        progress_bar.destroy()

        # Если это архив, распаковываем
        if file_path.endswith(".zip"):
            try:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    extract_path = os.path.join(SOFTWARE_DIR, os.path.basename(program['url']).replace('.zip', ''))
                    os.makedirs(extract_path, exist_ok=True)
                    zip_ref.extractall(extract_path)
                has_zip = program.get('zip')
                if has_zip:
                    with zipfile.ZipFile(os.path.join(SOFTWARE_DIR, os.path.basename(program['url'])).replace('.zip', ''), "r") as zip_ref:
                        extract_path = os.path.join(SOFTWARE_DIR, os.path.basename(program['url']).replace('.zip', ''), has_zip)
                        os.makedirs(extract_path, exist_ok=True)
                        zip_ref.extractall(extract_path)
                    
                QMessageBox.information(self, "Успех", f"Программа {program_name} успешно загружена и распакована.")
                self.launch_program(program_name)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка распаковки: {e}")
        else:
            QMessageBox.information(self, "Успех", f"Программа {program_name} успешно загружена.")

    def on_download_error(self, error_message, progress_bar: QProgressBar):
        progress_bar.destroy()
        QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {error_message}")












