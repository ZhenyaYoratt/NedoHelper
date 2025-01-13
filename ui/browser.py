from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import webbrowser
import validators
from modules.titles import make_title
import qtawesome
import qtmdi

def spin_icon(self):
    animation = qtawesome.Spin(self, autostart=True, step=5, interval=10)
    spin_icon = qtawesome.icon('mdi.loading', animation=animation)

    old_anim_update = animation._update
    def new_anim_update(self):
        old_anim_update()
    animation._update = new_anim_update.__get__(animation, qtawesome.Spin)
    return spin_icon

class BrowserWindow(QMainWindow):
    def __init__(self, parent = None, url = "https://www.google.com/?hl=ru"):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Встроенный браузер"))
        self.resize(1300, 840)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # Панель управления
        control_layout = QHBoxLayout()

        back_button = QPushButton()
        back_button.setIcon(qtawesome.icon("mdi.arrow-left"))
        back_button.setIconSize(QSize(28, 28))
        back_button.clicked.connect(lambda: self.current_tab().back())

        forward_button = QPushButton()
        forward_button.setIcon(qtawesome.icon("mdi.arrow-right"))
        forward_button.setIconSize(QSize(28, 28))
        forward_button.clicked.connect(lambda: self.current_tab().forward())

        reload_button = QPushButton()
        reload_button.setIcon(qtawesome.icon("mdi.reload"))
        reload_button.setIconSize(QSize(28, 28))
        reload_button.clicked.connect(lambda: self.current_tab().reload())

        home_button = QPushButton()
        home_button.setIcon(qtawesome.icon("mdi.home"))
        home_button.setIconSize(QSize(28, 28))
        home_button.clicked.connect(self.navigate_home)

        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Введите URL...")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.httpsicon = QLabel()

        go_button = QPushButton()
        go_button.setIcon(qtawesome.icon("mdi.arrow-right"))
        go_button.setIconSize(QSize(28, 28))
        go_button.clicked.connect(self.navigate_to_url)

        add_new_tab_button = QPushButton()
        add_new_tab_button.setIcon(qtawesome.icon("mdi.plus"))
        add_new_tab_button.setIconSize(QSize(28, 28))
        add_new_tab_button.clicked.connect(lambda: self.add_new_tab())


        # Кнопка с меню
        menu_button = QPushButton()
        menu_button.setIcon(qtawesome.icon("mdi.dots-vertical"))
        menu_button.setIconSize(QSize(28, 28))
        menu_button.setMenu(QMenu())
        menu_button.menu().addAction(qtawesome.icon("mdi.tab"), "Новая вкладка", lambda: self.add_new_tab())
        menu_button.menu().addAction(qtawesome.icon("mdi.shape-square-rounded-plus"), "Новое окно", lambda: BrowserWindow().show())
        menu_button.menu().addAction(qtawesome.icon("mdi.open-in-new"), "Открыть в стороннем браузере", self.open_in_external_browser)
        menu_button.menu().addAction(qtawesome.icon("mdi.exit-to-app"), "Закрыть", self.close)

        control_layout.addWidget(back_button)
        control_layout.addWidget(forward_button)
        control_layout.addWidget(reload_button)
        control_layout.addWidget(self.httpsicon)
        control_layout.addWidget(self.urlbar)
        control_layout.addWidget(go_button)
        control_layout.addWidget(add_new_tab_button)
        control_layout.addWidget(menu_button)

        layout.addLayout(control_layout)
        layout.addWidget(self.tabs)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.add_new_tab()

    def add_new_tab(self, qurl = QUrl('https://www.google.com/?hl=ru'), label ="Новая вкладка"):
        browser = QWebEngineView()
 
        browser.setUrl(qurl)

        # problem: js Unrecognized feature: 'cross-origin-isolated'.
        browser.page().setFeaturePermission(QUrl(), QWebEnginePage.Feature.WebRTC, QWebEnginePage.PermissionGrantedByUser)
 
        i = self.tabs.addTab(browser, spin_icon(self), label)
        self.tabs.setCurrentIndex(i)
 
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
        
        browser.titleChanged.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
        browser.loadStarted.connect(lambda i = i, browser = browser: 
                                     self.tabs.setTabIcon(i, spin_icon(self))
                                    )
        
        browser.loadFinished.connect(lambda _, i = i, browser = browser: (
                                     self.tabs.setTabText(i, browser.page().title()),
                                     self.tabs.setTabIcon(i, browser.page().icon())
                                    ))
        
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()
 
    def current_tab_changed(self, i):
        qurl = self.current_tab().url()
        self.update_urlbar(qurl, self.current_tab())
 
    def close_current_tab(self, i):
        self.tabs.removeTab(i)
        if self.tabs.count() < 1:
            self.close()

    def navigate_home(self):
        self.current_tab().setUrl(QUrl("https://www.google.com/?hl=ru"))
 
    def navigate_to_url(self):
        url = self.urlbar.text()
        if not url:
            url = self.urlbar.text().strip()
        if not validators.url(url):
            url = "https://www.google.com/search?q=" + url
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        q = QUrl(url)
        if q.scheme() == "":
            q.setScheme("http")
        self.current_tab().setUrl(q)
 
    def update_urlbar(self, q, browser = None):
        if browser != self.current_tab():
            return
        url = q.toString()
        self.urlbar.setText(url)
        self.urlbar.setCursorPosition(0)
        if url.startswith("https://"):
            # Secure padlock icon
            self.httpsicon.setPixmap(qtawesome.icon("fa.lock").pixmap(16, 16))
        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(qtawesome.icon("fa.unlock").pixmap(16, 16))

        # easter egg
        if url.find("nedohackers.site/challenge") != -1:
            QMessageBox.question(
                self,
                "а?",
                "Ваш сайт не работает... Потому что, вы напоставили капчов на всех устройствах",
                QMessageBox.StandardButton.Ignore | QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Help
            )
        if url.replace('+', '').replace('%20', '').find("simpleunlocker") != -1:
            QMessageBox.question(
                self,
                "зачееем",
                "Э! Я для кого запихнул SimpleUnlocker в прогу?! Посмотри в \"Запуске стороних программ\"!1",
                QMessageBox.StandardButton.Ignore | QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Help
            )

    def current_tab(self) -> QWebEngineView:
        return self.tabs.currentWidget()

    def open_in_external_browser(self):
        """Открывает URL в стороннем браузере."""
        url: str = self.urlbar.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webbrowser.open(url)
