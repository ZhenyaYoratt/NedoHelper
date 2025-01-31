from logging import log as llog, Handler, getLogger, DEBUG as DDEBUG, Formatter, StreamHandler
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
import colorlog

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
SUCCESS = 25
INFO = 20
DEBUG = 10
NOTSET = 0

level_colors = {
    NOTSET: "grey",
    DEBUG: "#3f4042",
    INFO: "#4fc1ff",
    SUCCESS: "green",
    WARNING: "yellow",
    ERROR: "red",
    CRITICAL: "bold_red",
}

level_colors_str = {
    'DEBUG': "black",
    'INFO': "cyan",
    'SUCCESS': "green",
    'WARNING': "yellow",
    'ERROR': "red",
    'CRITICAL': "bold_red",
}

def log(message, level=INFO):
    """Логирует сообщение с уровнем."""
    llog(level, message)

class QTextEditLogger(Handler):
    def __init__(self, text_edit_widget):
        super().__init__()
        self.text_edit_widget: QTextEdit = text_edit_widget

    def emit(self, record):
        msg = self.format(record)
        level = record.levelno
        try:
            self.text_edit_widget.setHtml(self.text_edit_widget.toHtml() + f'\n<span style="color: {level_colors[level]};{"font-weight: 900;" if level == CRITICAL else ""}; line-height: 1;">{msg}</span>')
            self.text_edit_widget.moveCursor(QTextCursor.MoveOperation.End)
        except RuntimeError:
            pass
        
def setup_logger(text_edit_widget):
    """
    Настраивает логгер для вывода в текстовое поле PyQt5.
    
    :param text_edit_widget: Виджет QPlainTextEdit, куда будут выводиться логи.
    """
    logger = getLogger()
    logger.setLevel(DDEBUG)

    # Очистка предыдущих обработчиков
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Создание обработчика для вывода в текстовое поле
    text_handler = QTextEditLogger(text_edit_widget)
    text_handler.setFormatter(Formatter('[%(levelname)s] %(message)s'))

    logger.addHandler(text_handler)

    # Также добавляем вывод в консоль (опционально)
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s [%(levelname)s] %(message)s',
        log_colors=level_colors_str
    ))
    logger.addHandler(console_handler)
