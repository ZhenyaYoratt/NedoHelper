from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QFileDialog
from antivirus import scan_directory, delete_file

class AntivirusWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Антивирус")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()
        self.status_label = QLabel("Антивирус: готов к работе.")
        self.results_label = QLabel("Результаты сканирования будут здесь.")
        start_scan_button = QPushButton("Сканировать папку")
        start_scan_button.clicked.connect(self.start_scan)

        layout.addWidget(self.status_label)
        layout.addWidget(start_scan_button)
        layout.addWidget(self.results_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_scan(self):
        """Начинает сканирование выбранной папки."""
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку для сканирования")
        if not directory:
            self.status_label.setText("Сканирование отменено.")
            return

        self.status_label.setText(f"Сканирование: {directory}...")
        suspicious_files = scan_directory(directory)
        if not suspicious_files:
            self.results_label.setText("Угроз не обнаружено.")
        else:
            results_text = "Найдены подозрительные файлы:\n" + "\n".join(suspicious_files)
            self.results_label.setText(results_text)
            for file in suspicious_files:
                delete_file(file)  # Удаляем подозрительные файлы
            self.status_label.setText("Сканирование завершено.")
