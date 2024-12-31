from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
import json

class SettingsWindow(QMainWindow):
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.status_label = QLabel("Настройки программы.")
        self.setting_input = QLineEdit()
        self.setting_input.setPlaceholderText("Введите настройку...")

        save_button = QPushButton("Сохранить настройку")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.status_label)
        layout.addWidget(self.setting_input)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_settings(self):
        """Сохраняет настройки в файл."""
        setting_value = self.setting_input.text().strip()
        if not setting_value:
            self.status_label.setText("Ошибка: значение настройки не указано.")
            return

        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump({"setting": setting_value}, file)
            self.status_label.setText("Настройки успешно сохранены.")
        except Exception as e:
            self.status_label.setText(f"Ошибка сохранения: {e}")
