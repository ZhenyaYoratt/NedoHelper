from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget, QHBoxLayout, QProgressBar
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser
from modules.titles import make_title

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title("Встроенный браузер"))
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Панель управления
        control_layout = QHBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.browser.back)

        forward_button = QPushButton("Вперёд")
        forward_button.clicked.connect(self.browser.forward)

        reload_button = QPushButton("Обновить")
        reload_button.clicked.connect(self.browser.reload)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите URL...")
        go_button = QPushButton("Перейти")
        go_button.clicked.connect(self.load_url)

        # Кнопка открытия в стороннем браузере
        external_browser_button = QPushButton("Открыть в стороннем браузере")
        external_browser_button.clicked.connect(self.open_in_external_browser)

        control_layout.addWidget(back_button)
        control_layout.addWidget(forward_button)
        control_layout.addWidget(self.url_input)
        control_layout.addWidget(go_button)
        control_layout.addWidget(external_browser_button)

        # Браузер
        self.browser = QWebEngineView()

        self.browser.urlChanged.connect(self.on_url_changed)
        self.browser.titleChanged.connect(self.on_title_changed)
        self.browser.loadStarted.connect(self.on_load_started)
        self.browser.loadFinished.connect(self.on_load_finished)

        self.progess_bar = QProgressBar()
        self.progess_bar.setTextVisible(False)
        self.progess_bar.setValue(0)

        layout.addLayout(control_layout)
        layout.addWidget(self.browser)
        layout.addWidget(self.progess_bar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_url_changed(self):
        self.url_input.setText(self.browser.url().toString())

    def on_title_changed(self):
        self.setWindowTitle(self.browser.title())

    def on_load_started(self):
        self.progess_bar.setRange(0, 0)
    def on_load_finished(self):
        self.progess_bar.setRange(0, 1)

    def load_url(self):
        """Загружает указанный URL."""
        url = self.url_input.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def open_in_external_browser(self):
        """Открывает URL в стороннем браузере."""
        url = self.url_input.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webbrowser.open(url)
