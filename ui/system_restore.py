from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt
from modules.system_restore import create_restore_point, restore_to_point
from modules.titles import make_title

class SystemRestoreWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title("Точка восстановления"))
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout()
        self.status_label = QLabel("Управление точками восстановления.")
        create_restore_button = QPushButton("Создать точку восстановления")
        create_restore_button.clicked.connect(self.create_restore_point)

        restore_button = QPushButton("Восстановить систему")
        restore_button.clicked.connect(self.restore_system)

        layout.addWidget(self.status_label)
        layout.addWidget(create_restore_button)
        layout.addWidget(restore_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_restore_point(self):
        """Создает точку восстановления."""
        result = create_restore_point()
        self.status_label.setText(result)

    def restore_system(self):
        """Восстанавливает систему к точке восстановления."""
        result = restore_to_point()
        self.status_label.setText(result)
