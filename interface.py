from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

import sys
import classeslib as classlib 

env_size = 50
window_height = 800
window_width = 600
window_top = 150
window_left = 150
window_title = "Evolution simulation"

class mywindow(QtWidgets.QMainWindow):

    def addAnimal(self, x, y, energy):
        self.animals.append(classlib.Animal(x,y,energy))

    def update(self, animals, enviroment):
        for animal in animals:
            animal.update(enviroment)
            time.sleep(0.7)

    def paintEvent(self, event):
        qpainter = QPainter(self)
        self.enviroment.draw(qpainter)

    def __init__(self):
    
        super().__init__()

        self.top = window_top
        self.left = window_left
        self.height = window_height
        self.width = window_width
        self.title = window_title
        self.animals = []
        self.enviroment = classlib.Enviroment(env_size, env_size, window_width/env_size)

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.show()

app = QtWidgets.QApplication([])

application = mywindow()

application.addAnimal(0,0,100)
print(application.enviroment.Tiles[0].size)

sys.exit(app.exec())
