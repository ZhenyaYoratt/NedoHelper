from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import psutil
from modules.disk_manager import *
from modules.titles import make_title
from pyqt_windows_os_light_dark_theme_window.main import Window

class DiskManagerWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title('Управление дисками'))
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout()

        self.header_label = QLabel("Список дисков")
        self.header_label.setObjectName("title")

        self.click_label = QLabel("Клик по диску для открытия меню")

        self.disk_table = QTableWidget()
        self.disk_table.setColumnCount(6)
        self.disk_table.setHorizontalHeaderLabels(["Буква", "Наименование", "BitLocker", "Занято/Свободно", "Статус", "Тип"])
        self.disk_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.disk_table.setSelectionBehavior(self.disk_table.SelectRows)
        self.disk_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.disk_table.itemClicked.connect(self.open_disk_menu)

        layout.addWidget(self.header_label)
        layout.addWidget(self.click_label)
        layout.addWidget(self.disk_table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.resize(1200, 400)

        self.refresh_disk_list()

    def open_disk_menu(self, item: QListWidgetItem):
        row = item.row()
        disk_letter = self.disk_table.item(row, 0).text()
        disk_name = self.disk_table.item(row, 1).text()

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Управление диском {disk_letter} ({disk_name})")
        dialog.setFixedSize(400, 200)
        dialog.move(self.cursor().pos())
        layout = QVBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(get_disk_icon(disk_letter))
        letter_label = QLabel(f"{disk_letter}")
        letter_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        unlock_bitlocker_button = QPushButton("Разблокировать BitLocker")
        unlock_bitlocker_button.clicked.connect(lambda: unlock_bitlocker(disk_letter))
        layout.addWidget(icon_label)
        layout.addWidget(letter_label)
        layout.addWidget(unlock_bitlocker_button)
        dialog.setLayout(layout)
        dialog.exec()

    def refresh_disk_list(self):
        """Обновляет список дисков."""
        partitions = psutil.disk_partitions()
        self.disk_table.setRowCount(len(partitions))

        for row, partition in enumerate(partitions):
            # Диск
            self.disk_table.setItem(row, 0, QTableWidgetItem(partition.device))

            # Название (имя устройства)
            self.disk_table.setItem(row, 1, QTableWidgetItem(get_volume_name(partition.device)))

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