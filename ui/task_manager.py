from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from modules.task_manager import get_process_list, get_process_type, Process
from modules.titles import make_title
from psutil import boot_time

def parse_precents(value):
    return f"{value:.1f}%" if value is not None else "0.0%"

def parse_create_time(value):
    return QDateTime.fromSecsSinceEpoch(int(value)).toString(Qt.DateFormat.ISODate)

class ProcessListWorker(QObject):
    process_list_updated = pyqtSignal(list)
    update_interval = 1

    def run(self):
        while True:
            self.refresh_process_list()
            QThread.msleep(int(self.update_interval * 1000))

    def refresh_process_list(self):
        self.process_list_updated.emit(get_process_list())

class TaskManagerWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Диспетчер задач"))
        self.resize(1000, 700)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setStyleSheet(self.styleSheet() + "QPushButton { padding: 0px 4px; }")

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Диспетчер задач"))

        view_button = QPushButton("Вид")
        view_button.setMenu(QMenu(self))
        view_button.menu().addAction("Обновить сейчас", self.refresh_process_list)
        update_interval_menu = view_button.menu().addMenu("Скорость обновления")
        update_interval_menu.addAction("Очень быстро — 0.1 сек", lambda: self.set_update_interval(0.5))
        update_interval_menu.addAction("Быстро — 0.5 секунд", lambda: self.set_update_interval(0.5))
        update_interval_menu.addAction("Обычная — 1 секунд", lambda: self.set_update_interval(1))
        update_interval_menu.addAction("Низкая — 3 секунд", lambda: self.set_update_interval(5))
        update_interval_menu.addAction("Очень низкая — 5 секунд", lambda: self.set_update_interval(5))
        update_interval_menu.addAction("Черепаха — 10 секунд", lambda: self.set_update_interval(10))
        view_button.menu().addSeparator()
        hide_critical_processes_action = view_button.menu().addAction("Скрыть критические процессы", self.toggle_critical_processes)
        hide_critical_processes_action.setCheckable(True)
        hide_system_processes_action = view_button.menu().addAction("Скрыть системные процессы", self.toggle_system_processes)
        hide_system_processes_action.setCheckable(True)
        hide_system_processes_action.setChecked(True)

        # Поиск
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Поиск названия, файла, PID...')
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.textChanged.connect(lambda text: self.filter_process_list(text))

        boot_time_label = QLabel(f"Время загрузки: {QDateTime.fromSecsSinceEpoch(int(boot_time())).toString(Qt.DateFormat.ISODate)}")

        top_layout.addWidget(view_button)
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(boot_time_label)

        # Таблица процессов
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(8)
        self.process_table.setHorizontalHeaderLabels(["Имя процесса", "ЦП", "ОЗУ", "Состояние", "PID", "Тип", "Действия с процессом", "Создано"])
        self.process_table.setSelectionBehavior(self.process_table.SelectRows)
        self.process_table.setEditTriggers(self.process_table.NoEditTriggers)

        layout.addLayout(top_layout)
        layout.addWidget(self.process_table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Таймер обновления списка процессов
        self._worker = ProcessListWorker()
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._worker.process_list_updated.connect(lambda process_list: self.update_process_list(process_list))
        self._thread.started.connect(self._worker.run)
        self._thread.start()
        
        self.process_list_ui = []
        self.process_list = []

        self.hide_critical_processes = False
        self.hide_system_processes = True

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Диспетчер задач запущен.")

    def closeEvent(self, a0):
        self._thread.quit()
        return super().closeEvent(a0)
    
    def set_update_interval(self, interval):
        self._worker.update_interval = interval

    def toggle_critical_processes(self):
        self.hide_critical_processes = not self.hide_critical_processes
        self.filter_process_list()

    def toggle_system_processes(self):
        self.hide_system_processes = not self.hide_system_processes
        self.filter_process_list()

    def filter_process_list(self, search_text = None):
        """Фильтрует список процессов по имени процесса, имя файла или PID."""
        if search_text:
            self.process_list_ui = [process for process in self.process_list if search_text.lower() in process.name.lower() or search_text in str(process.pid)]
        if self.hide_critical_processes:
            self.process_list_ui = [process for process in self.process_list_ui if process.process_type != 'critical']
        if self.hide_system_processes:
            self.process_list_ui = [process for process in self.process_list_ui if process.process_type != 'system']
        return self.refresh_process_list()
    
    def update_process_list(self, process_list):
        self.process_list = process_list
        if self.search_bar.text():
            self.filter_process_list(self.search_bar.text())
        else:
            self.process_list_ui = self.process_list
        self.filter_process_list()

    def refresh_process_list(self):
        """Обновляет список процессов."""
        count = len(self.process_list)
        count_ui = len(self.process_list_ui)
        self.statusBar().showMessage("Всего: " + str(count) + ". Показано процессов: " + str(count_ui) + " (из них скрыты: " + str(count - count_ui) + ")")
        self.process_table.setRowCount(count_ui)
        for row, process in enumerate(self.process_list_ui):
            process: Process = process
            item = QTableWidgetItem(process.name)
            item.setIcon(QIcon(process.get_process_icon()))
            self.process_table.setItem(row, 0, item)
            self.process_table.setItem(row, 1, QTableWidgetItem(parse_precents(process.cpu_percent) if process.pid != 0 else None))
            self.process_table.setItem(row, 2, QTableWidgetItem(parse_precents(process.memory_percent)))
            self.process_table.setItem(row, 3, QTableWidgetItem(Process.STATUS[process.status]))
            self.process_table.setItem(row, 4, QTableWidgetItem(str(process.pid)))
            self.process_table.setItem(row, 5, QTableWidgetItem(Process.PROCESS_TYPE[process.process_type]))
            self.process_table.setItem(row, 7, QTableWidgetItem(parse_create_time(process.create_time)))
            actions = QWidget()
            layout_actions = QHBoxLayout()
            terminate_button = QPushButton('Завершить')
            terminate_button.clicked.connect(process.kill)
            suspend_button = QPushButton('Приостановить')
            suspend_button.clicked.connect(process.suspend)
            resume_button = QPushButton('Возобновить')
            resume_button.clicked.connect(process.resume)
            layout_actions.addWidget(terminate_button)
            layout_actions.addWidget(suspend_button)
            layout_actions.addWidget(resume_button)
            layout_actions.setContentsMargins(0, 0, 0, 0)
            actions.setLayout(layout_actions)
            actions.setContentsMargins(0, 0, 0, 0)
            self.process_table.setItem(row, 6, QTableWidgetItem())
            self.process_table.setCellWidget(row, 6, actions)
        self.process_table.resizeColumnsToContents()
        self.process_table.resizeRowsToContents()

