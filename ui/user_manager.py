from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from modules.user_manager import list_users, add_user, delete_user, set_password
from modules.titles import make_title

class UserManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(make_title("Управление пользователями"))
        self.setFixedSize(500, 500)

        layout = QVBoxLayout()
        self.status_label = QLabel("Управление пользователями.")
        self.users_label = QLabel("Список пользователей будет здесь.")
        list_users_button = QPushButton("Показать пользователей")
        list_users_button.clicked.connect(self.show_users)

        # Добавление пользователя
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        add_user_button = QPushButton("Добавить пользователя")
        add_user_button.clicked.connect(self.add_user)

        # Удаление пользователя
        self.delete_user_input = QLineEdit()
        self.delete_user_input.setPlaceholderText("Имя пользователя для удаления")
        delete_user_button = QPushButton("Удалить пользователя")
        delete_user_button.clicked.connect(self.delete_user)

        # Установка пароля
        self.set_password_input = QLineEdit()
        self.set_password_input.setPlaceholderText("Имя пользователя для пароля")
        set_password_button = QPushButton("Установить пароль")
        set_password_button.clicked.connect(self.set_password)

        layout.addWidget(self.status_label)
        layout.addWidget(list_users_button)
        layout.addWidget(self.users_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(add_user_button)
        layout.addWidget(self.delete_user_input)
        layout.addWidget(delete_user_button)
        layout.addWidget(self.set_password_input)
        layout.addWidget(set_password_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_users(self):
        users = list_users()
        self.users_label.setText(users)

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        result = add_user(username, password)
        self.status_label.setText(result)

    def delete_user(self):
        username = self.delete_user_input.text().strip()
        if QMessageBox.question(self, "Подтверждение", f"Удалить пользователя {username}?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            result = delete_user(username)
            self.status_label.setText(result)

    def set_password(self):
        username = self.set_password_input.text().strip()
        password = self.password_input.text().strip()
        result = set_password(username, password)
        self.status_label.setText(result)
