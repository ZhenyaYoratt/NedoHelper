from subprocess import Popen, PIPE
from .logger import *
from PyQt5.QtCore import QObject, pyqtSignal

class ProcessLauncher(QObject):
    process_output = pyqtSignal(str, str)

    def __init__(self, parent, command):
        super().__init__()
        self.setParent(parent)
        self.command = command

    def launch_process(self):
        """Запускает процесс с опциональными правами администратора."""
        try:
            process = Popen(self.command, shell=True, stdout=PIPE, stderr=PIPE, text=True, encoding='cp866')
            stdout, stderr = process.communicate()
            self.process_output.emit(stdout, stderr)
        except Exception as e:
            msg = f"Ошибка запуска процесса `{self.command}`: {e}"
            log(msg, ERROR)
            self.process_output.emit("", msg)