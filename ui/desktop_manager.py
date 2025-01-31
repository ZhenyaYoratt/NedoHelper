from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QListWidget, QListView, QPushButton, QHBoxLayout, QWidget, QFileDialog, QListWidgetItem, QStatusBar
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from modules.desktop_manager import set_wallpaper, reset_wallpaper
from modules.titles import make_title
from modules.logger import *
import os
from pyqt_windows_os_light_dark_theme_window.main import Window

DEFAULT_WALLPAPER = "C:/Windows/Web/Wallpaper/Windows/img0.jpg"
WALLPAPERS_FOLDER = "C:/Windows/Web/Wallpaper/"

class DesktopManagerWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Управление обоями"))
        self.resize(700, 700)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Готов к работе")

        layout = QVBoxLayout()
        self.header_label = QLabel("Управление обоями рабочего стола.")
        self.header_label.setObjectName("title")

        # A list of all wallpapers in folder with previews; clicking on a preview sets the wallpaper
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListView.ViewMode.IconMode)
        self.list_widget.setIconSize(QSize(320, 200))
        self.list_widget.doubleClicked.connect(lambda: set_wallpaper(self.list_widget.currentItem().path))

        change_wallpaper_button = QPushButton("Выбрать файл обоев")
        change_wallpaper_button.clicked.connect(self.change_wallpaper)

        reset_wallpaper_button = QPushButton("Поставить дефолтные обои")
        reset_wallpaper_button.clicked.connect(lambda: set_wallpaper(DEFAULT_WALLPAPER))

        black_color_wallpaper_button = QPushButton("Удалить обои")
        black_color_wallpaper_button.clicked.connect(self.reset_wallpaper)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(reset_wallpaper_button)
        buttons_layout.addWidget(black_color_wallpaper_button)

        layout.addWidget(self.header_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(change_wallpaper_button)
        layout.addLayout(buttons_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_wallpapers()

    def update_wallpapers(self):
        """Обновляет список обоев в папке."""
        # use os.walk() to get all wallpapers in subfolders
        for root, _, files in os.walk(WALLPAPERS_FOLDER):
            for file in files:
                if file.endswith((".jpg", ".jpeg", ".png", ".bmp")):
                    item = QListWidgetItem()
                    item.setText(file)
                    item.setIcon(QIcon(os.path.join(root, file)))
                    item.path = os.path.join(root, file)
                    self.list_widget.addItem(item)

    def change_wallpaper(self):
        """Меняет обои рабочего стола."""
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not image_path:
            log("Обои не выбраны.", WARN)
            return

        self.statusbar.showMessage(set_wallpaper(image_path))

    def reset_wallpaper(self):
        """Сбрасывает обои рабочего стола."""
        self.statusbar.showMessage(reset_wallpaper())
