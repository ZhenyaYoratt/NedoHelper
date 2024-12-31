from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget
from task_manager import get_process_list, kill_process

class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кастомный диспетчер задач")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Таблица процессов
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(2)
        self.process_table.setHorizontalHeaderLabels(["Имя процесса", "PID"])
        self.process_table.setSelectionBehavior(self.process_table.SelectRows)
        layout.addWidget(self.process_table)

        # Кнопки управления
        refresh_button = QPushButton("Обновить список")
        refresh_button.clicked.connect(self.refresh_process_list)
        kill_button = QPushButton("Завершить процесс")
        kill_button.clicked.connect(self.terminate_selected_process)

        layout.addWidget(refresh_button)
        layout.addWidget(kill_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.refresh_process_list()

    def refresh_process_list(self):
        """Обновляет список процессов."""
        process_list = get_process_list()
        self.process_table.setRowCount(len(process_list))
        for row, (process_name, pid) in enumerate(process_list):
            self.process_table.setItem(row, 0, QTableWidgetItem(process_name))
            self.process_table.setItem(row, 1, QTableWidgetItem(str(pid)))

    def terminate_selected_process(self):
        """Завершает выбранный процесс."""
        selected_row = self.process_table.currentRow()
        if selected_row < 0:
            return
        pid = self.process_table.item(selected_row, 1).text()
        result = kill_process(int(pid))
        self.refresh_process_list()
