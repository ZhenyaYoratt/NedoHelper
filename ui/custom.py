from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer, Qt, QElapsedTimer, QSize
from PyQt5.QtGui import QPainter

class MarqueeLabel(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(parent)
        self._offset = 0
        self._text_width = 0
        self._space_width = 0  # Ширина пробела между текстами
        self.speed = 50  # Скорость в пикселях в секунду
        self.setText(text)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setStyleSheet("background-color: transparent;")

        # Таймер для плавной анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateOffset)
        self.elapsed_timer = QElapsedTimer()
        self.timer.start(int(1/75*1000))  # Около 75 FPS
        self.elapsed_timer.start()

    def updateOffset(self):
        total_width = self._text_width + self._space_width
        if total_width > self.width():
            delta = self.elapsed_timer.restart() / 1000  # Время между кадрами в секундах
            self._offset -= self.speed * delta
            if self._offset < -total_width:
                self._offset = 0  # Сброс к началу
            self.update()
        else:
            self._offset = 0  # Сброс смещения, если текст помещается
            self.update()

    def setText(self, text):
        super().setText(text)
        self._text_width = self.fontMetrics().width(self.text())
        self._space_width = self.fontMetrics().width(' ') * 10  # Ширина пробела между текстами
        self._offset = 0  # Сброс смещения при изменении текста
        self.update()

    def resizeEvent(self, event):
        self._text_width = self.fontMetrics().width(self.text())
        self._space_width = self.fontMetrics().width(' ') * 10
        self._offset = 0
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        total_width = self._text_width

        if total_width > self.width():
            # Рисуем текст с учетом смещения
            x = self._offset
            y = self.height() // 2 + self.fontMetrics().ascent() // 2
            painter.drawText(round(x), round(y), self.text())
            # Дублируем текст с пробелом для бесшовного эффекта
            painter.drawText(round(x + total_width + self._space_width), round(y), self.text())
        else:
            # Если текст помещается, рисуем его по центру
            painter.drawText(self.rect(), Qt.AlignLeft | Qt.AlignVCenter, self.text())

    def sizeHint(self):
        return super().sizeHint()

    def minimumSizeHint(self):
        return QSize(1, self.fontMetrics().height())