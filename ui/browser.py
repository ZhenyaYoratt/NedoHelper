from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTabWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMenu, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser
import validators
from modules.titles import make_title
import qtawesome
from pyqt_windows_os_light_dark_theme_window.main import Window

def spin_icon(self):
    animation = qtawesome.Spin(self, autostart=True, step=5, interval=10)
    spin_icon = qtawesome.icon('mdi.loading', animation=animation)

    old_anim_update = animation._update
    def new_anim_update(self):
        old_anim_update()
    animation._update = new_anim_update.__get__(animation, qtawesome.Spin)
    return spin_icon

class BrowserWindow(QMainWindow, Window):
    def __init__(self, parent = None, url = "https://www.google.com/?hl=ru"):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title(self.tr("Встроенный браузер")))
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

        self.back_button = QPushButton()
        self.back_button.setIcon(qtawesome.icon("mdi.arrow-left"))
        self.back_button.setIconSize(QSize(28, 28))
        self.back_button.clicked.connect(lambda: self.current_tab().back())

        self.forward_button = QPushButton()
        self.forward_button.setIcon(qtawesome.icon("mdi.arrow-right"))
        self.forward_button.setIconSize(QSize(28, 28))
        self.forward_button.clicked.connect(lambda: self.current_tab().forward())

        self.reload_button = QPushButton()
        self.reload_button.setIcon(qtawesome.icon("mdi.reload"))
        self.reload_button.setIconSize(QSize(28, 28))
        self.reload_button.clicked.connect(lambda: self.current_tab().reload())

        self.home_button = QPushButton()
        self.home_button.setIcon(qtawesome.icon("mdi.home"))
        self.home_button.setIconSize(QSize(28, 28))
        self.home_button.clicked.connect(self.navigate_home)

        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText(self.tr("Введите URL..."))
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.httpsicon = QLabel()

        self.go_button = QPushButton()
        self.go_button.setIcon(qtawesome.icon("mdi.arrow-right"))
        self.go_button.setIconSize(QSize(28, 28))
        self.go_button.clicked.connect(self.navigate_to_url)

        self.add_new_tab_button = QPushButton()
        self.add_new_tab_button.setIcon(qtawesome.icon("mdi.plus"))
        self.add_new_tab_button.setIconSize(QSize(28, 28))
        self.add_new_tab_button.clicked.connect(lambda: self.add_new_tab())


        # Кнопка с меню
        self.menu_button = QPushButton()
        self.menu_button.setIcon(qtawesome.icon("mdi.dots-vertical"))
        self.menu_button.setIconSize(QSize(28, 28))
        self.menu_button.setMenu(QMenu())
        self.menu_button.menu().addAction(qtawesome.icon("mdi.tab"), self.tr("Новая вкладка"), lambda: self.add_new_tab())
        self.menu_button.menu().addAction(qtawesome.icon("mdi.shape-square-rounded-plus"), self.tr("Новое окно"), lambda: BrowserWindow().show())
        self.menu_button.menu().addAction(qtawesome.icon("mdi.incognito"), self.tr("Новое окно в режиме инкогнито"), self.open_incognito_mode)
        self.menu_button.menu().addSeparator()
        self.menu_button.menu().addAction(qtawesome.icon("mdi.history"), self.tr("История"), self.show_history)
        self.menu_button.menu().addAction(qtawesome.icon("mdi.bookmark"), self.tr("Закладки"), self.show_bookmarks)
        self.menu_button.menu().addAction(qtawesome.icon("mdi.download"), self.tr("Загрузки"), self.show_downloads)
        self.menu_button.menu().addSeparator()
        self.menu_button.menu().addAction(qtawesome.icon("mdi.open-in-new"), self.tr("Открыть в стороннем браузере"), self.open_in_external_browser)
        self.menu_button.menu().addAction(qtawesome.icon("mdi.exit-to-app"), self.parent().tr("Выход"), self.close)

        control_layout.addWidget(self.back_button)
        control_layout.addWidget(self.forward_button)
        control_layout.addWidget(self.reload_button)
        control_layout.addWidget(self.httpsicon)
        control_layout.addWidget(self.urlbar)
        control_layout.addWidget(self.go_button)
        control_layout.addWidget(self.add_new_tab_button)
        control_layout.addWidget(self.menu_button)

        layout.addLayout(control_layout)
        layout.addWidget(self.tabs)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.add_new_tab(self.get_qurl(url))

    def add_new_tab(self, qurl = QUrl('https://www.google.com/?hl=ru'), label ="New Tab"):
        browser = QWebEngineView()
 
        browser.setUrl(qurl)
 
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
        url = self.urlbar.text().strip()
        self.current_tab().setUrl(self.get_qurl(url))

    def get_qurl(self, url):
        if not validators.url(url):
            url = "https://www.google.com/search?q=" + url
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        q = QUrl(url)
        if q.scheme() == "":
            q.setScheme("http")
        return q
 
    def update_urlbar(self, q, browser = None):
        if browser != self.current_tab():
            return
        url: str = q.toString()
        self.urlbar.setText(url)
        if not self.urlbar.hasFocus():
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
                "Ваш сайт не работает... Потому что, вы напоставили капчов везде",
                QMessageBox.StandardButton.Ignore | QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Help
            )
        if url.replace('+', '').replace('%20', '').replace(' ', '').lower().find("simpleunlocker") != -1:
            QMessageBox.question(
                self,
                "зачееем",
                "Э! Я для кого запихнул SimpleUnlocker в прогу?! Посмотри в \"Запуске стороних программ\"!!1",
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

    def open_incognito_mode(self):
        """Открывает новое окно в режиме инкогнито."""
        incognito_window = BrowserWindow()
        QMessageBox.information(self, self.tr("Режим инкогнито"), self.tr("Данная функция еще не реализована."))
        incognito_window.setWindowTitle(make_title(self.tr("Режим инкогнито")))
        incognito_window.show()

    def show_history(self):
        """Показывает историю браузера."""
        QMessageBox.information(self, self.tr("История"), self.tr("Данная функция еще не реализована."))

    def show_bookmarks(self):
        """Показывает закладки браузера."""
        QMessageBox.information(self, self.tr("Закладки"), self.tr("Данная функция еще не реализована."))

    def show_downloads(self):
        """Показывает загрузки браузера."""
        QMessageBox.information(self, self.tr("Загрузки"), self.tr("Данная функция еще не реализована."))

    def retranslateUi(self):
        self.setWindowTitle(make_title(self.tr("Встроенный браузер")))
        self.menu_button.menu().actionAt(0).setText(self.tr("Новая вкладка"))
        self.menu_button.menu().actionAt(1).setText(self.tr("Новое окно"))
        self.menu_button.menu().actionAt(2).setText(self.tr("Новое окно в режиме инкогнито"))
        self.menu_button.menu().actionAt(3).setText(self.tr("История"))
        self.menu_button.menu().actionAt(4).setText(self.tr("Закладки"))
        self.menu_button.menu().actionAt(5).setText(self.tr("Загрузки"))
        self.menu_button.menu().actionAt(6).setText(self.tr("Открыть в стороннем браузере"))
        self.menu_button.menu().actionAt(7).setText(self.parent().tr("Выход"))