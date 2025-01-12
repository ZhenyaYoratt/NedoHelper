from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QFileDialog, QWidget
from PyQt5.QtCore import Qt
from modules.desktop_manager import set_wallpaper, reset_wallpaper
from modules.titles import make_title
from modules.logger import *

class DesktopManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title("Управление обоями"))
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout()
        self.status_label = QLabel("Управление обоями рабочего стола.")
        change_wallpaper_button = QPushButton("Выбрать файл обоев")
        change_wallpaper_button.clicked.connect(self.change_wallpaper)

        reset_wallpaper_button = QPushButton("Сбросить обои")
        reset_wallpaper_button.clicked.connect(self.reset_wallpaper)

        layout.addWidget(self.status_label)
        layout.addWidget(change_wallpaper_button)
        layout.addWidget(reset_wallpaper_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def change_wallpaper(self):
        """Меняет обои рабочего стола."""
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not image_path:
            log("Обои не выбраны.", WARN)
            return

        set_wallpaper(image_path)

    def reset_wallpaper(self):
        """Сбрасывает обои рабочего стола."""
        reset_wallpaper()
