from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QProgressBar
from PyQt5.QtCore import Qt
import psutil
from modules.disk_manager import *
from modules.titles import make_title

class DiskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title('Управление дисками'))
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout()
        self.disk_table = QTableWidget()
        self.disk_table.setColumnCount(6)
        self.disk_table.setHorizontalHeaderLabels(["Буква диска", "Название", "Битлокер", "Занято/Свободно", "Статус", "Тип"])

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
            bitlocker_status = is_bitlocker_protected(partition.device)  
            self.disk_table.setItem(row, 2, QTableWidgetItem("Да" if bitlocker_status == True else "Нет" if bitlocker_status == False else "N/A"))

            # Прогресс бар
            progress = QProgressBar()
            self.disk_table.setCellWidget(row, 3, progress)

            disk_status = check_disk_status(partition.mountpoint)
            if disk_status:
                usage = psutil.disk_usage(partition.mountpoint)
                progress.setValue(int((usage.used / usage.total) * 100))
            else:
                progress.setDisabled(True)
            
            # Доступность
            self.disk_table.setItem(row, 4, QTableWidgetItem("ОК" if disk_status else "Недоступен"))
            
            # Тип
            self.disk_table.setItem(row, 5, QTableWidgetItem(get_disk_type(partition.mountpoint)))

        self.disk_table.resizeColumnsToContents()
        self.disk_table.resizeRowsToContents()