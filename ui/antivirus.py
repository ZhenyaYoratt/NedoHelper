from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QProgressBar, QListWidget, QFileDialog, QWidget
from modules.antivirus import delete_file, UpdateWorker, ScanThread
from modules.titles import make_title
from pyqt_windows_os_light_dark_theme_window.main import Window

class AntivirusWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Антивирус"))
        self.setMaximumSize(800, 1000)
        self.resize(450, 350)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Готов к работе")

        layout = QVBoxLayout()
        update_db_button = QPushButton("Обновить базы данных")
        update_db_button.clicked.connect(self.update_db)

        self.header_label = QLabel("Антивирус")
        self.header_label.setObjectName("title")

        self.progress_bar = QProgressBar()
        self.results_label = QLabel("Результаты сканирования:")
        self.results_list = QListWidget()
        start_scan_button = QPushButton("Сканировать папку")
        start_scan_button.clicked.connect(self.start_scan)

        self.statusbar.addPermanentWidget(self.progress_bar)

        layout.addWidget(self.header_label)
        layout.addWidget(update_db_button)
        layout.addWidget(start_scan_button)
        layout.addWidget(self.results_label)
        layout.addWidget(self.results_list)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_db(self):
        self.statusbar.showMessage("Обновление базы данных...")
        self.progress_bar.setValue(0)
        self.worker = UpdateWorker()
        self.worker.set_max.connect(self.progress_bar.setMaximum)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.completed.connect(lambda: (
            self.statusbar.showMessage("Базы данных обновлены!"),
            self.progress_bar.setMaximum(1),
            self.progress_bar.reset()
        ))
        thread = QThread(self.parent())
        self.worker.moveToThread(thread)
        thread.started.connect(self.worker.run)
        thread.start()

    def start_scan(self):
        """Начинает сканирование выбранной папки."""
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку для сканирования")
        if not directory:
            self.statusbar.showMessage("Сканирование отменено.")
            return

        self.statusbar.showMessage(f"Сканирование: {directory}...")
        self.progress_bar.setValue(0)
        self._thread = ScanThread(directory)
        self._thread.set_max.connect(self.progress_bar.setMaximum)
        self._thread.progress.connect(self.progress_bar.setValue)
        self._thread.suspicious_file.connect(self.results_list.addItem)
        self._thread.completed.connect(self.complete_scan)
        self._thread.run()

    def complete_scan(self, suspicious_files):
        self.progress_bar.setMaximum(1)
        self.progress_bar.reset()
        if not suspicious_files:
            self.statusbar.showMessage("Угроз не обнаружено.")
        else:
            self.statusbar.showMessage("Сканирование завершено.")
            results_text = "Найдены подозрительные файлы:"
            self.results_list.clear()
            self.results_list.addItems(suspicious_files)
            #for file in suspicious_files:
            #    delete_file(file)  # Удаляем подозрительные файлы
