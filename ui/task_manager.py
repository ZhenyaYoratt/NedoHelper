from PyQt5.QtWidgets import *
from modules.task_manager import get_process_list, kill_process, parse_process_info
from modules.titles import make_title

class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title("Диспетчер задач"))
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Таблица процессов
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["Имя процесса", "PID", "Статус", "Действия"])
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
        for row, process in enumerate(process_list):
            pid, name, status = parse_process_info(process)
            self.process_table.setItem(row, 0, QTableWidgetItem(name))
            self.process_table.setItem(row, 1, QTableWidgetItem(str(pid)))
            self.process_table.setItem(row, 2, QTableWidgetItem(status))
            actions = QWidget()
            layout_actions = QHBoxLayout()
            terminate_button = QPushButton('Завершить')
            terminate_button.clicked.connect(lambda: kill_process(pid))
            suspend_button = QPushButton('Приостановить')
            resume_button = QPushButton('Возобновить')
            layout_actions.addWidget(terminate_button)
            layout_actions.addWidget(suspend_button)
            layout_actions.addWidget(resume_button)
            actions.setLayout(layout_actions)
            self.process_table.setItem(row, 3, QTableWidgetItem())
            self.process_table.setCellWidget(row, 3, actions)
        self.process_table.resizeColumnsToContents()
        self.process_table.resizeRowsToContents()

    def terminate_selected_process(self):
        """Завершает выбранный процесс."""
        selected_row = self.process_table.currentRow()
        if selected_row < 0:
            return
        pid = self.process_table.item(selected_row, 1).text()
        result = kill_process(int(pid))
        self.refresh_process_list()
