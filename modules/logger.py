import datetime
import logging

from PyQt5.QtWidgets import QTextEdit

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

level_colors = {
    NOTSET: "grey",
    DEBUG: "black",
    INFO: "blue",
    WARNING: "yellow",
    ERROR: "red",
}

def log(message, level=INFO):
    """Логирует сообщение с уровнем."""
    logging.log(level, message)

class QTextEditLogger(logging.Handler):
    def __init__(self, text_edit_widget):
        super().__init__()
        self.text_edit_widget: QTextEdit = text_edit_widget

    def emit(self, record):
        msg = self.format(record)
        level = record.levelno
        self.text_edit_widget.setHtml(self.text_edit_widget.toHtml() + f'\n<div style="color: {level_colors[level]};{"font-weight: 900;" if level == CRITICAL else None}">{msg}</div>')

def setup_logger(text_edit_widget):
    """
    Настраивает логгер для вывода в текстовое поле PyQt5.
    
    :param text_edit_widget: Виджет QPlainTextEdit, куда будут выводиться логи.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Очистка предыдущих обработчиков
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Создание обработчика для вывода в текстовое поле
    text_handler = QTextEditLogger(text_edit_widget)
    text_handler.setFormatter(logging.Formatter(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' [%(levelname)s]	%(message)s'))

    logger.addHandler(text_handler)

    # Также добавляем вывод в консоль (опционально)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]	%(message)s'))
    logger.addHandler(console_handler)
