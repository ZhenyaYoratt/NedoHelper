from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt
import json
from modules.titles import make_title

class SettingsWindow(QMainWindow):
    SETTINGS_FILE = "settings.json"

    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Настройки"))
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Готов к работе")

        layout = QVBoxLayout()
        self.header_label = QLabel("Настройки программы.")
        self.header_label.setObjectName("title")
        self.setting_input = QLineEdit()
        self.setting_input.setPlaceholderText("Введите настройку...")

        save_button = QPushButton("Сохранить настройку")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.header_label)
        layout.addWidget(self.setting_input)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_settings(self):
        """Сохраняет настройки в файл."""
        setting_value = self.setting_input.text().strip()
        if not setting_value:
            self.statusbar.showMessage("Ошибка: значение настройки не указано.")
            return

        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump({"setting": setting_value}, file)
            self.statusbar.showMessage("Настройки успешно сохранены.")
        except Exception as e:
            self.statusbar.showMessage(f"Ошибка сохранения: {e}")
