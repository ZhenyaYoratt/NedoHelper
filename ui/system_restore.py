from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt
from modules.system_restore import create_restore_point, restore_to_point
from modules.titles import make_title
from pyqt_windows_os_light_dark_theme_window.main import Window

class SystemRestoreWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Точка восстановления"))
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout()
        self.header_label = QLabel("Управление точками восстановления.")
        self.header_label.setObjectName("title")
        create_restore_button = QPushButton("Создать точку восстановления")
        create_restore_button.clicked.connect(self.create_restore_point)

        restore_button = QPushButton("Восстановить систему")
        restore_button.clicked.connect(self.restore_system)

        layout.addWidget(self.header_label)
        layout.addWidget(create_restore_button)
        layout.addWidget(restore_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_restore_point(self):
        """Создает точку восстановления."""
        result = create_restore_point()
        self.statusbar.showMessage(result)

    def restore_system(self):
        """Восстанавливает систему к точке восстановления."""
        result = restore_to_point()
        self.statusbar.showMessage(result)
