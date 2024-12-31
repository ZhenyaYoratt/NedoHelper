from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Встроенный браузер")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Панель управления
        control_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите URL...")
        go_button = QPushButton("Перейти")
        go_button.clicked.connect(self.load_url)

        control_layout.addWidget(self.url_input)
        control_layout.addWidget(go_button)

        # Браузер
        self.browser = QWebEngineView()

        # Кнопка открытия в стороннем браузере
        external_browser_button = QPushButton("Открыть в стороннем браузере")
        external_browser_button.clicked.connect(self.open_in_external_browser)

        layout.addLayout(control_layout)
        layout.addWidget(self.browser)
        layout.addWidget(external_browser_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_url(self):
        """Загружает указанный URL."""
        url = self.url_input.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(url)

    def open_in_external_browser(self):
        """Открывает URL в стороннем браузере."""
        url = self.url_input.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webbrowser.open(url)
