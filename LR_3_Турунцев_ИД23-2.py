from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton,  QLineEdit, QVBoxLayout, QDialog
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QTimer
from PyQt5 import QtWidgets, QtGui
import random


class Dialogue(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Диалоговое окно")
        
        # Создаем вертикальный layout
        layout = QVBoxLayout()
        
    # Добавляем поля ввода position, size, droplet_density, droplet_speed
        self.position_label = QLabel("Введите позицию x y:")
        self.position_input = QLineEdit()
        
        self.size_label = QLabel("Введите размер:")
        self.size_input = QLineEdit()
        
        self.droplet_density_label = QLabel("Введите плотность капель (с 0 до 1):")
        self.droplet_density_input = QLineEdit()
        
        self.droplet_speed_label = QLabel("Введите скорость капель:")
        self.droplet_speed_input = QLineEdit()

        self.figure_type = QLabel("Введите тип тучки:\n1 - Овал\n2 - Прямоугольник\n3 - Винни Пух:")
        self.figure_type_input = QLineEdit()





        
    # Добавляем кнопку OK
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)  # Закрывает диалог при нажатии
        
    # Добавляем элементы в layout
        layout.addWidget(self.position_label)
        layout.addWidget(self.position_input)
        
        layout.addWidget(self.size_label)
        layout.addWidget(self.size_input)
        
        layout.addWidget(self.droplet_density_label)
        layout.addWidget(self.droplet_density_input)
        
        layout.addWidget(self.droplet_speed_label)
        layout.addWidget(self.droplet_speed_input)

        layout.addWidget(self.figure_type)
        layout.addWidget(self.figure_type_input)
        
        layout.addWidget(self.ok_button)
        
        self.setLayout(layout)

class App(QMainWindow):
            

    def __init__(self):
        super().__init__()
        self.widthApp, self.heightApp = 800, 800
        self.setStyleSheet("background-color: white;")
                              

        self.initUI()
        self.poslits = []

        self.Clouds = []

        self.current_cloud=None
        self.current_pos=None



        self.show()

        

        
    def create_Winnie(self, x, y):
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("C:/Users/petrt/Desktop/VS_Projects/LR_3/v.jpg"))  # Change this to your image path
        self.image_label.setScaledContents(True)  # Scale the image to fit the label
        self.image_label.setFixedSize(100, 100)  
        self.image_label.move(x - 50, y - 50)
        self.image_label.show()

    def initUI(self):
        Add_Cloud_btn = QPushButton("Add Cloud", self)
        Add_Cloud_btn.setStyleSheet("background-color: blue; color: white;")
        Add_Cloud_btn.move(0, 0)

        Delete_Cloud_btn = QPushButton("Delete Cloud", self)
        Delete_Cloud_btn.move(100, 0)
        Delete_Cloud_btn.setStyleSheet("background-color: red; color: white;")

        Add_Cloud_btn.clicked.connect(self.Add_Cloud_btn_clicked)
        Delete_Cloud_btn.clicked.connect(self.Delete_Cloud_btn_clicked)
        
    
        self.setGeometry(600, 300, self.width(), self.height())

        self.show()
    
    
    def Add_Cloud_btn_clicked(self):

        class Cloud():

            def __init__(self, position, size, droplet_density, droplet_speed, upd):
                self.position = position
                self.size = size
                self.droplet_density = droplet_density
                self.droplet_speed = droplet_speed
                self.figure_type = 1

                self.drops_fixed = []
                self.upd = upd
                

                self.timer = QTimer()
                self.timer.timeout.connect(self.updateDrops)
                self.timer.start(30)


            def paint(self, painter):
                painter.setBrush(QtGui.QColor(255, 255, 255))
                if self.figure_type == 1:
                    painter.drawEllipse(self.position[0], self.position[1], self.size + 20, self.size)

                if self.figure_type == 2:
                    painter.drawRect(self.position[0], self.position[1], self.size, self.size)

                if self.figure_type == 3:
                    pixmap = QPixmap(r'C:\Users\petrt\Desktop\VS_Projects\LR_3\vvv.png')
                    painter.drawPixmap(self.position[0], self.position[1], self.size, self.size, pixmap)
                
                
            

                painter.setBrush(QtGui.QColor(0, 0, 255))
                for drop in self.drops_fixed:
                    painter.drawRect(drop[0], drop[1], drop[2], drop[3]) 


            def updateDrops(self, bias = random.randint(-1, 1)):

                if random.random() < self.droplet_density:  # С вероятностью добавляем новую каплю
                    x = random.randint(self.position[0], self.position[0] + self.size - 10)
                    self.drops_fixed.append([x, self.position[1] + self.size, 2, self.size // 3])  # Начальная позиция капли

                for drop in self.drops_fixed:
                        drop[1] += self.droplet_speed   # Двигаем капли вниз
                        drop[0] += 3

                self.drops_fixed = [drop for drop in self.drops_fixed if drop[1] < 800]  # Удаляем капли за пределами экрана   
                self.upd()        

            def open_dialog(self, event):
                dialog = Dialogue()
                if dialog.exec_() == QDialog.Accepted:
                    self.position = [int(i) for i in dialog.position_input.text().split()]
                    print(self.position)
                    self.size = int(dialog.size_input.text())
                    self.droplet_density = float(dialog.droplet_density_input.text())
                    self.droplet_speed = int(dialog.droplet_speed_input.text())
                    self.figure_type = int(dialog.figure_type_input.text())
            




        new_cloud = Cloud([100, 50], 50, 1, 10, self.update)

        self.Clouds.append(new_cloud)
        self.update()
    
    
    def Delete_Cloud_btn_clicked(self):
        self.Clouds = self.Clouds[:len(self.Clouds)-1]
        self.update()
    

    def paintEvent(self, event):
        painter = QPainter(self)
        for cloud in self.Clouds:
            cloud.paint(painter)


 

        
    


    

    def mousePressEvent(self, event):
        
        if event.button() == Qt.RightButton:  # Проверяем нажатие левой кнопки мыши
            for cloud in self.Clouds:
                rect_area = QRect(cloud.position[0], cloud.position[1], cloud.size, cloud.size)
                if rect_area.contains(event.pos()):  # Проверяем, попадает ли клик в область
                    cloud.open_dialog(event)

                else:
                    pass

        if event.button() == Qt.LeftButton:
            for cloud in self.Clouds:
                rect_area = QRect(cloud.position[0], cloud.position[1], cloud.size, cloud.size)
                if rect_area.contains(event.pos()):  # Проверяем, попадает ли клик в область
                    self.current_cloud = cloud



    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            self.current_cloud.position = (int(x), int(y)) 
    

    





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = App()
    sys.exit(app.exec_())

