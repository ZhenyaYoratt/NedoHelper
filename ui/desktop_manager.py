from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QFileDialog, QWidget
from modules.desktop_manager import set_wallpaper, reset_wallpaper
from modules.titles import make_title

class DesktopManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title("Управление обоями"))
        self.setFixedSize(400, 300)

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
            self.status_label.setText("Обои не выбраны.")
            return

        result = set_wallpaper(image_path)
        self.status_label.setText(result)

    def reset_wallpaper(self):
        """Сбрасывает обои рабочего стола."""
        result = reset_wallpaper()
        self.status_label.setText(result)
