from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from modules.user_manager import list_users, add_user, delete_user, set_password
from modules.titles import make_title
from modules.logger import *
from pyqt_windows_os_light_dark_theme_window.main import Window

class UserManagerWindow(QMainWindow, Window):
    def __init__(self, parent = None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(make_title("Управление пользователями"))
        self.setFixedSize(500, 500)
        self.setWindowFlags(Qt.WindowType.Dialog)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Готов к работе")

        layout = QVBoxLayout()
        self.header_label = QLabel("Управление пользователями")
        self.header_label.setObjectName("title")
        label = QLabel("Клик по пользователю для просмотра информации")
        self.users_view = QListWidget()
        self.users_view.itemClicked.connect(self.show_user_info)

        # Добавление пользователя
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        add_user_button = QPushButton("Добавить пользователя")
        add_user_button.clicked.connect(self.add_user)

        layout.addWidget(self.header_label)
        layout.addWidget(label)
        layout.addWidget(self.users_view)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(add_user_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_users()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_users)
        self.timer.start(5000)

    def closeEvent(self, a0):
        self.timer.stop()
        return super().closeEvent(a0)

    def show_user_info(self, item: QListWidgetItem):
        user = item.data(Qt.ItemDataRole.UserRole)
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Информация о пользователе {user.name}")
        dialog.setFixedSize(400, 200)
        dialog.move(self.cursor().pos())
        layout = QVBoxLayout()
        username_label = QLabel(f"Имя пользователя: {user.name}")
        terminal_label = QLabel(f"Терминал: {user.terminal if user.terminal else 'Неизвестно'}")
        host_label = QLabel(f"Хост: {user.host if user.host else 'Неизвестно'}")
        started_label = QLabel(f"Запущен: {QDateTime.fromSecsSinceEpoch(int(user.started)).toString()}")
        delete_user_button = QPushButton("Удалить пользователя")
        delete_user_button.clicked.connect(lambda: self.delete_user(user.name))
        set_password_button = QPushButton("Установить пароль")
        set_password_button.clicked.connect(lambda: self.set_password(user.name))
        layout.addWidget(username_label)
        layout.addWidget(terminal_label)
        layout.addWidget(host_label)
        layout.addWidget(started_label)
        layout.addWidget(delete_user_button)
        layout.addWidget(set_password_button)
        dialog.setLayout(layout)
        dialog.exec()

    def update_users(self):
        users = list_users()
        log(f"Пользователи: {users}", DEBUG)
        self.users_view.clear()
        for user in users:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, user)
            item.setText(f"{user.name}")
            self.users_view.addItem(item)

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        ok, result = add_user(username, password)
        self.statusbar.showMessage(result)
        self.username_input.clear()
        self.password_input.clear()
        if ok:
            QMessageBox.information(self, "Успешно", f"Пользователь {username} успешно добавлен. Однако требуется инциализация пользователя, чтобы показался в списке.")
        else:
            QMessageBox.warning(self, "Ошибка", f"Ошибка добавления пользователя {username}.")
        self.update_users()

    def delete_user(self, username: str):
        if QMessageBox.question(self, "Подтверждение", f"Удалить пользователя {username}?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            ok, result = delete_user(username)
            self.statusbar.showMessage(result)
            self.update_users()
            if ok:
                QMessageBox.information(self, "Успешно", f"Пользователь {username} успешно удален. Может потребоваться перезагрузить компьютер.")
            else:
                QMessageBox.warning(self, "Ошибка", f"Ошибка удаления пользователя {username}.")

    def set_password(self, username: str):
        password, ok = QInputDialog.getText(self, "Установка пароля", f"Введите новый пароль для пользователя {username}")
        if ok:
            ok, result = set_password(username, password)
            self.statusbar.showMessage(result)
            self.update_users()
            if ok:
                QMessageBox.information(self, "Успешно", f"Пароль для пользователя {username} успешно установлен.")
            else:
                QMessageBox.warning(self, "Ошибка", f"Ошибка установки пароля для пользователя {username}.")
