from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QProgressBar
import psutil
from modules.disk_manager import is_bitlocker_protected, check_disk_status
from modules.titles import make_title

class DiskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title('Управление дисками'))
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()
        self.disk_table = QTableWidget()
        self.disk_table.setColumnCount(4)
        self.disk_table.setHorizontalHeaderLabels(["Буква диска", "Название", "Битлокер", "Занято/Свободно"])

        layout.addWidget(self.disk_table)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.refresh_disk_list()

    def refresh_disk_list(self):
        """Обновляет список дисков."""
        partitions = psutil.disk_partitions()
        self.disk_table.setRowCount(len(partitions))

        for row, partition in enumerate(partitions):
            # Диск
            self.disk_table.setItem(row, 0, QTableWidgetItem(partition.device))

            # Название (имя устройства)
            self.disk_table.setItem(row, 1, QTableWidgetItem(partition.mountpoint))

            # Проверка на защиту BitLocker
            bitlocker_status = "Да" if is_bitlocker_protected(partition.device) else "Нет"
            self.disk_table.setItem(row, 2, QTableWidgetItem(bitlocker_status))

            # Прогресс бар
            progress = QProgressBar()
            self.disk_table.setCellWidget(row, 3, progress)
            if check_disk_status(partition.mountpoint):
                usage = psutil.disk_usage(partition.mountpoint)
                progress.setValue(int((usage.used / usage.total) * 100))
            else:
                progress.setDisabled(True)
        self.disk_table.resizeColumnsToContents()
        self.disk_table.resizeRowsToContents()