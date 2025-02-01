import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt
from modules.titles import make_title
from ui.browser import BrowserWindow
from pyqt_windows_os_light_dark_theme_window.main import Window

ABOUT_TEXT = """
Программа мультул позволит вам удалить вирусы (наверное) и восстановить Windows 10 до её идеального состояния. Эта программа разработана эксклюзивно для YouTube-канала "НЕДОХАКЕРЫ Lite".

Для получения дополнительной информации посетите <a href="https://github.com/ZhenyaYoratt/NedoHelper">GitHub репозиторий</a>.
"""

class AboutWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("О программе"))
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.header_label = QLabel('О программе', self)
        self.header_label.setObjectName('title')
        layout.addWidget(self.header_label)
        
        buttons_layout = QHBoxLayout()

        about_label = QLabel(self)
        about_label.setTextFormat(Qt.TextFormat.AutoText | Qt.TextFormat.RichText)
        about_label.setText(ABOUT_TEXT)
        about_label.linkActivated.connect(self.link_clicked)
        about_label.setWordWrap(True)
        layout.addWidget(about_label)

        about_qt_button = QPushButton('О Qt', self)
        about_qt_button.clicked.connect(QApplication.aboutQt)
        buttons_layout.addWidget(about_qt_button)

        close_button = QPushButton('Закрыть', self)
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)
        
        layout.addLayout(buttons_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def link_clicked(self, url):
        self.browser_window = BrowserWindow(self.parent(), url)
        self.browser_window.show()