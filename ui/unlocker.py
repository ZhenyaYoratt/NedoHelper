from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTabWidget, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QCheckBox, QHeaderView, QHBoxLayout, QStatusBar
from PyQt5.QtCore import Qt
from modules.titles import make_title
from modules.unlocker import run_scan, run_manual_unlock, keys_to_unlock
from pyqt_windows_os_light_dark_theme_window.main import Window

class UnlockerWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title(self.tr("Разблокировка ограничений")))
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.initUI()
        self.resize(800, 600)
        self.center()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.scan_tab = QWidget()
        self.manual_unlock_tab = QWidget()

        self.tabs.addTab(self.scan_tab, self.tr("Сканирование"))
        self.tabs.addTab(self.manual_unlock_tab, self.tr("Ручная разблокировка"))

        self.init_scan_tab()
        self.init_manual_unlock_tab()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def center(self):
        """Центрирует окно по центру экрана."""
        frame_geometry = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def init_scan_tab(self):
        scan_layout = QVBoxLayout()
        scan_label = QLabel(self.tr("Сканирование"))
        self.auto_unlock_checkbox = QCheckBox(self.tr("Автоматическая разблокировка ограничений"))
        self.scan_table = QTableWidget()
        self.scan_table.setColumnCount(3)
        self.scan_table.setHorizontalHeaderLabels([self.tr("Ограничение"), self.tr("Описание"), self.tr("Путь")])
        self.scan_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        scan_button = QPushButton(self.tr("Запустить сканирование"))
        scan_button.clicked.connect(self.run_scan)

        scan_layout.addWidget(scan_label)
        scan_layout.addWidget(self.auto_unlock_checkbox)
        scan_layout.addWidget(self.scan_table)
        scan_layout.addWidget(scan_button)
        self.scan_tab.setLayout(scan_layout)

    def init_manual_unlock_tab(self):
        manual_layout = QVBoxLayout()
        manual_label = QLabel(self.tr("Ручная разблокировка"))
        self.select_all_checkbox = QCheckBox(self.tr("Выбрать все"))
        self.select_all_checkbox.stateChanged.connect(self.select_all)
        self.manual_table = QTableWidget()
        self.manual_table.setColumnCount(2)
        self.manual_table.setHorizontalHeaderLabels([self.tr("Ограничение"), self.tr("Описание")])
        self.manual_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        manual_button = QPushButton(self.tr("Разблокировать"))
        manual_button.clicked.connect(self.run_manual_unlock)

        self.manual_table.setRowCount(len(keys_to_unlock))
        for row, (key, description, _) in enumerate(keys_to_unlock):
            checkbox = QCheckBox(key)
            checkbox.data = (key, description, _)
            layout = QHBoxLayout()
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            widget = QWidget()
            widget.setLayout(layout)
            self.manual_table.setCellWidget(row, 0, widget)
            self.manual_table.setItem(row, 1, QTableWidgetItem(description))

        manual_layout.addWidget(manual_label)
        manual_layout.addWidget(self.select_all_checkbox)
        manual_layout.addWidget(self.manual_table)
        manual_layout.addWidget(manual_button)
        self.manual_unlock_tab.setLayout(manual_layout)

    def run_scan(self):
        self.status_bar.showMessage(self.tr("Сканирование..."))
        results = run_scan()
        self.scan_table.setRowCount(len(results))
        for row, (key, description, path) in enumerate(results):
            self.scan_table.setItem(row, 0, QTableWidgetItem(key))
            self.scan_table.setItem(row, 1, QTableWidgetItem(description))
            self.scan_table.setItem(row, 2, QTableWidgetItem(path))
        if self.auto_unlock_checkbox.isChecked():
            run_manual_unlock(results)
            self.status_bar.showMessage(self.tr("Сканирование и разблокировка завершена!"), 5000)
        else:
            self.status_bar.showMessage(self.tr("Сканирование завершено!"), 5000)

    def run_manual_unlock(self):
        self.status_bar.showMessage(self.tr("Разблокировка..."))
        keys_to_unlock = []
        for row in range(self.manual_table.rowCount()):
            checkbox = self.manual_table.cellWidget(row, 0).layout().itemAt(0).widget()
            if checkbox.isChecked():
                keys_to_unlock.append(checkbox.data)
        print(keys_to_unlock)
        run_manual_unlock(keys_to_unlock)
        self.status_bar.showMessage(self.tr("Разблокировка завершена"), 5000)

    def select_all(self, state):
        for row in range(self.manual_table.rowCount()):
            checkbox = self.manual_table.cellWidget(row, 0).layout().itemAt(0).widget()
            checkbox.setChecked(state == Qt.Checked)
