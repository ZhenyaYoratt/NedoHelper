from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QListWidget, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from modules.system_restore import create_restore_point, restore_to_point, list_restore_points, is_system_protection_enabled, toggle_system_protection
from modules.titles import make_title
from pyqt_windows_os_light_dark_theme_window.main import Window

class SystemRestoreWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title(self.parent().tr("Точка восстановления")))
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.statusbar = self.statusBar()

        layout = QVBoxLayout()
        self.header_label = QLabel(self.tr("Управление точками восстановления"))
        self.header_label.setObjectName("title")

        protect_layout = QHBoxLayout()
        self.protect_label = QLabel(self.tr("Защита системы") + ": " + (self.tr("Да") if is_system_protection_enabled() else self.tr("Нет")))
        self.protect_toggle = QPushButton('Переключить защиту')
        self.protect_toggle.clicked.connect(toggle_system_protection)
        protect_layout.addWidget(self.protect_label)
        protect_layout.addWidget(self.protect_toggle)

        self.list = QListWidget()

        self.create_restore_button = QPushButton(self.tr("Создать точку восстановления"))
        self.create_restore_button.clicked.connect(self.create_restore_point)

        self.restore_button = QPushButton(self.tr("Восстановить систему"))
        self.restore_button.setMinimumSize(200, 50)
        self.restore_button.clicked.connect(self.restore_system)
        self.restore_button.setEnabled(False)

        layout.addWidget(self.header_label)
        layout.addLayout(protect_layout)
        layout.addWidget(self.list)
        layout.addWidget(self.create_restore_button)
        layout.addWidget(self.restore_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_list()

    def update_list(self):
        """Обновляет список точек восстановления."""
        self.list.clear()
        points = list_restore_points()
        self.list.addItems(points)
        self.statusbar.showMessage(self.tr("Точки восстановления обновлены. Всего: {0}").format(len(points)))
        self.list.itemSelectionChanged.connect(self.clicked)
        self.statusbar.showMessage(self.tr("Точки восстановления обновлены. Всего: {0}").format(len(points)) if len(points) > 0 else self.tr("Нет точек восстановления"))

    def clicked(self):
        indexes = self.list.selectedIndexes()
        self.restore_button.setEnabled(len(indexes) > 0)

    def create_restore_point(self):
        """Создает точку восстановления."""
        result = create_restore_point()
        self.statusbar.showMessage(self.tr("Точка восстановления создана") if result else self.tr("Ошибка создания точки восстановления"))

    def restore_system(self):
        """Восстанавливает систему к точке восстановления."""
        indexes = self.list.selectedIndexes()
        if len(indexes) > 1:
            return QMessageBox().warning(self, self.tr("Ошибка"), self.tr("Выберите только одну точку восстановления!"))
        result = restore_to_point(indexes[0])
        self.statusbar.showMessage(self.tr("Система восстановлена к точке восстановления") if result else self.tr("Ошибка восстановления системы"))

    def retranslateUi(self):
        self.setWindowTitle(make_title(self.parent().tr("Точка восстановления")))
        self.header_label.setText(self.tr("Управление точками восстановления"))
        self.create_restore_button.setText(self.tr("Создать точку восстановления"))
        self.restore_button.setText(self.tr("Восстановить систему"))
