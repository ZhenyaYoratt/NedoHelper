import os, shutil, subprocess, sys
from PyQt5.QtWidgets import (
    QApplication, QWizard, QWizardPage, QVBoxLayout, QRadioButton, QMessageBox,
    QPushButton, QLabel, QFileDialog, QLineEdit
)
from PyQt5.QtCore import Qt

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    
main_exe = "NedoHelper.exe"  # Имя файла программы

class InstallerWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Установщик программы")
        self.setFixedSize(500, 300)

        # Страницы мастера
        self.addPage(self.create_intro_page())
        self.addPage(self.create_install_page())
        self.addPage(self.create_finish_page())

        # Путь установки
        self.install_path = ""

    def create_intro_page(self):
        page = QWizardPage()
        page.setTitle("Добро пожаловать")
        page.setSubTitle("Добро пожаловать")

        layout = QVBoxLayout()
        label = QLabel("Добро пожаловать в установщик программы!")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)

        self.prepare_system_radio = QRadioButton("Установить программу и подготовить систему")
        self.open_program_radio = QRadioButton("Просто открыть программу")
        self.open_program_radio.setChecked(True)

        layout.addWidget(self.prepare_system_radio)
        layout.addWidget(self.open_program_radio)

        page.setLayout(layout)
        return page

    def create_install_page(self):
        page = QWizardPage()
        page.setTitle("Выбор пути установки")

        layout = QVBoxLayout()
        self.path_label = QLabel("Путь установки:")
        layout.addWidget(self.path_label)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Выберите папку установки")
        self.path_input.setReadOnly(True)
        layout.addWidget(self.path_input)

        self.browse_button = QPushButton("Обзор")
        self.browse_button.clicked.connect(self.select_install_path)
        layout.addWidget(self.browse_button)

        page.setLayout(layout)
        return page

    def create_finish_page(self):
        page = QWizardPage()
        page.setTitle("Завершение")

        layout = QVBoxLayout()
        self.finish_label = QLabel()
        layout.addWidget(self.finish_label)

        page.setLayout(layout)
        return page

    def select_install_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку установки")
        if folder:
            self.install_path = folder
            self.path_input.setText(folder)

    def accept(self):
        if self.prepare_system_radio.isChecked():
            if not self.install_path:
                QMessageBox.warning(self, "Внимание!", "Выберите папку перед установкой!")
                return
            self.prepare_system()
        else:
            self.open_program()
        super().accept()

    def prepare_system(self):
        if not os.path.isfile(main_exe):
            QMessageBox.critical(self, "Ошибка!", "Программа не найдена!")
            return

        try:
            os.makedirs(self.install_path, exist_ok=True)
            target_path = os.path.join(self.install_path, main_exe)
            shutil.copy(os.path.join(application_path, main_exe), target_path)
            QMessageBox.information(self, "Установка завершена!", f"Программа установлена в: {self.install_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка установки!", f"{e}")

    def open_program(self):
        try:
            subprocess.Popen(os.path.join(application_path, main_exe))
        except:
            QMessageBox.critical(self, "Ошибка запуска!", "Не удалось запустить программу! Попробуйте установить его.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = InstallerWizard()
    wizard.show()

    sys.exit(app.exec_())
