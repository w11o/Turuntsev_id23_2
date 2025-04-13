import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore


class RainDrop(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.drops_fixed = []
        self.drops_random = []
        self.lightnings = []
        self.drop_count = 0


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setBrush(QtGui.QColor(0, 0, 255))

        for drop in self.drops_fixed:
            painter.drawRect(drop[0], drop[1], drop[2], drop[3])  # Рисуем капли дождя

        for drop in self.drops_random:
            painter.drawRect(drop[0], drop[1], drop[2], drop[3])  # Рисуем капли дождя

        painter.setPen(QtGui.QColor('yellow'))

        if self.drop_count % 8 == 0:
            # Определяем точки для молнии
            lightning = [
                QtCore.QPoint(50, 50),
                QtCore.QPoint(70, 80),
                QtCore.QPoint(50, 100),
                QtCore.QPoint(90, 100),
                QtCore.QPoint(70, 180)
            ]

            # Рисуем полилинию
            painter.drawPolyline(lightning)

        painter.setPen(QtGui.QColor('white'))
        painter.drawText(10, 20, f"Количество капель: {self.drop_count}")



    def updateDrops(self, bias = random.randint(-1, 1), speed = random.randint(20, 50)):

        if random.random() < 0.9:  # С вероятностью добавляем новую каплю
            x = random.randint(0, self.width())
            self.drops_fixed.append([x, 0, 2, 20])  # Начальная позиция капли
            self.drop_count += 1
        for drop in self.drops_fixed:
                drop[1] += 20  # Двигаем капли вниз
                drop[0] += 5


        if random.random() < random.randint(0, 1):  # С вероятностью добавляем новую каплю
            x = random.randint(0, self.width())
            self.drops_random.append([x, 0, random.randint(2, 4), random.randint(30, 40)])
            self.drop_count += 1
        for drop in self.drops_random:
                drop[1] += speed  # Двигаем капли вниз
                drop[0] += bias







        self.drops_fixed = [drop for drop in self.drops_fixed if drop[1] < self.height()]  # Удаляем капли за пределами экрана
        self.drops_random = [drop for drop in self.drops_random if drop[1] < self.height()]
        self.update()  # Перерисовываем виджет


class RainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.rain = RainDrop()
        self.setCentralWidget(self.rain)
        self.setWindowTitle("Дождь")
        self.setStyleSheet("background-color: black;")

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.rain.updateDrops)
        timer.start(30)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RainApp()
    window.show()
    sys.exit(app.exec_())
