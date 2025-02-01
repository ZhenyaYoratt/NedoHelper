import os
import traceback
import zipfile
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox, QWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QThread, QByteArray, QObject, QSize
from PyQt5.QtGui import QIcon, QPixmap
from modules.titles import make_title
from pyqt_windows_os_light_dark_theme_window.main import Window
import qtawesome

# Ссылки для загрузки программ
SOFTWARE_URLS = {
    "ProcessHacker": {
        "url": "https://raw.githubusercontent.com/ZhenyaYoratt/NedoHelper/refs/heads/main/hosted_softwares/processhacker-2.39-bin.zip",
        "path": "x64/ProcessHacker.exe",
        "icon": "https://www.softportal.com/scr/14593/icons/process_hacker_72.png"
    },
    "Explorer++": {
        "url": "https://download.explorerplusplus.com/stable/1.4.0/explorerpp_x64.zip",
        "path": "Explorer++.exe",
        "icon": "https://explorerplusplus.com/images/favicon.ico"
    },
    "AnVir Task Manager": {
        "url": "https://www.anvir.net/downloads/anvirrus.zip",
        "path": "anvirrus-portable/AnVir.exe",
        "zip": "anvirrus-portable.zip",
        "icon": "https://www.softportal.com/scr/9259/icons/anvir_task_manager_72.png"
    },
    "Autoruns": {
        "url": "https://download.sysinternals.com/files/Autoruns.zip",
        "path": "Autoruns.exe",
        "icon": "https://www.softportal.com/scr/7891/icons/autoruns_72.png"
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
        "icon": "https://www.softportal.com/scr/47453/icons/regcool_64.png"
    },
    "RegAlyzer": {
        "url": "https://download2.portableapps.com/portableapps/RegAlyzerPortable/RegAlyzerPortable_1.6.2.16.paf.exe",
    },
    "Total Commander": {
        "url": "https://totalcommander.ch/1103/tcmd1103x32_64.exe",
        "icon": "https://www.softportal.com/scr/33/icons/total_commander_72.png"
    },
    "CCleaner": {
        "url": "https://download.ccleaner.com/portable/ccsetup631.zip",
        "path": "CCleaner.exe",
        "icon": "https://www.softportal.com/scr/14259/icons/ccleaner_portable_72.png"
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

class AsyncQIcon(QObject):
    icon_downloaded = pyqtSignal(QIcon)

    def __init__(self, url, placeholder_icon=None, parent=None):
        super().__init__(parent)
        self.url = url
        self.placeholder_icon = placeholder_icon or QIcon()
        self.manager = QNetworkAccessManager(parent)

    def download_icon(self):
        request = QNetworkRequest(QUrl(self.url))
        self.reply = self.manager.get(request)
        self.reply.finished.connect(self.on_finished)

    def on_finished(self):
        reply = self.reply
        if reply.error() == QNetworkReply.NetworkError.NoError:
            pixmap = QPixmap()
            data: QByteArray = reply.readAll()
            if pixmap.loadFromData(data):
                icon = QIcon(pixmap)
                self.icon_downloaded.emit(icon)
            else:
                self.icon_downloaded.emit(self.placeholder_icon)
        else:
            self.icon_downloaded.emit(self.placeholder_icon)
        reply.deleteLater()

class SoftwareLauncher(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Запуск сторонних программ"))
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
        header_label.setObjectName("title")
        layout.addWidget(header_label)

        placeholder_icon = QIcon("ui/icons/placeholder.png")

        # Кнопки для запуска и удаления программ
        self.buttons = {}
        for program_name in SOFTWARE_URLS.keys():
            button_layout = QHBoxLayout()
            button = QPushButton(program_name)
            if SOFTWARE_URLS[program_name].get('icon'):
                icon = AsyncQIcon(SOFTWARE_URLS[program_name]['icon'], placeholder_icon, self.parent())
                icon.icon_downloaded.connect(lambda icon, b=button: b.setIcon(icon))
                icon.download_icon()
                button.setIcon(placeholder_icon)
                button.setIconSize(QSize(24, 24))
            button.clicked.connect(lambda checked, p=program_name: self.launch_program(p))
            button_layout.addWidget(button)

            delete_button = QPushButton()
            delete_button.setIcon(qtawesome.icon("fa.trash", color="red"))
            delete_button.clicked.connect(lambda checked, p=program_name: self.delete_program(p))
            delete_button.setMaximumSize(28, 28)
            button_layout.addWidget(delete_button)

            layout.addLayout(button_layout)
            self.buttons[program_name] = (button, delete_button)
            self.update_delete_button_state(program_name)

    def update_delete_button_state(self, program_name):
        program = SOFTWARE_URLS.get(program_name)
        program_dir = os.path.abspath(os.path.join(SOFTWARE_DIR, os.path.basename(program['url']).replace('.zip', '')))
        delete_button = self.buttons[program_name][1]
        delete_button.setEnabled(os.path.exists(program_dir))

    def launch_program(self, program_name):
        program = SOFTWARE_URLS.get(program_name)
        program_dir = os.path.abspath(os.path.join(SOFTWARE_DIR, os.path.basename(program['url']).replace('.zip', '')))

        # Проверяем наличие программы
        if not os.path.exists(program_dir):
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
            path = os.path.join(program_dir, program['path'])
            os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить программу {program_name}.\n{e}\n\nПопробуйте удалить и скачать завоно.")

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
        progress_bar.setFormat(f"Загрузка {program_name}... %p%")

        self.worker = DownloadSoftwareWorker(self, program['url'], file_path)
        self.worker.set_max.connect(progress_bar.setMaximum)
        self.worker.progress.connect(progress_bar.setValue)
        self.worker.completed.connect(lambda path: self.on_download_completed(path, program_name, program, progress_bar))
        self.worker.error.connect(lambda error: self.on_download_error(error, progress_bar))
        thread = QThread(self.parent())
        self.worker.moveToThread(thread)
        thread.started.connect(self.worker.run)
        thread.start()

    def on_download_completed(self, file_path: str, program_name: str, program: dict, progress_bar: QProgressBar):
        progress_bar.deleteLater()

        # Если это архив, распаковываем
        if file_path.endswith(".zip"):
            try:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    extract_path = os.path.join(SOFTWARE_DIR, os.path.basename(program['url']).replace('.zip', ''))
                    os.makedirs(extract_path, exist_ok=True)
                    zip_ref.extractall(extract_path)
                os.remove(file_path)  # Удаляем архив после распаковки
                QMessageBox.information(self, "Успех", f"Программа {program_name} успешно загружена и распакована.")
                self.launch_program(program_name)
            except Exception as e:
                msg = QMessageBox()
                msg.setDetailedText(traceback.format_exc())
                msg.critical(self, "Ошибка", f"Ошибка распаковки: {e}")
        else:
            QMessageBox.information(self, "Успех", f"Программа {program_name} успешно загружена.")
        self.update_delete_button_state(program_name)

    def on_download_error(self, error_message, progress_bar: QProgressBar):
        progress_bar.deleteLater()
        QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {error_message}")

    def delete_program(self, program_name):
        program = SOFTWARE_URLS.get(program_name)
        program_dir = os.path.abspath(os.path.join(SOFTWARE_DIR, os.path.basename(program['url']).replace('.zip', '')))

        if os.path.exists(program_dir):
            try:
                for root, dirs, files in os.walk(program_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(program_dir)
                QMessageBox.information(self, "Успех", f"Программа {program_name} успешно удалена.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить программу {program_name}.\n{e}\n\nВозможно, программа запущена.")
        else:
            QMessageBox.information(self, "Информация", f"Программа {program_name} не найдена.")
        self.update_delete_button_state(program_name)












