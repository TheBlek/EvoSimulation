from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

import time
import sys
import classeslib as classlib 

window_height = 800
window_width = 600
window_top = 150
window_left = 150
window_title = "Evolution simulation"
turn_delay = 0
env_size = 50
tile_size = window_width / env_size
animal_size = tile_size / 2

class mywindow(QtWidgets.QMainWindow):

    def addAnimal(self, x, y, energy):
        self.animals.append(classlib.Animal(x,y,energy, animal_size, self.enviroment))

    def updateAnimals(self):
        for animal in self.animals:
            animal.update()
            time.sleep(turn_delay)
        self.update()


    def paintEvent(self, event):
        qpainter = QPainter(self)
        #qpainter.begin(self)
        self.enviroment.draw(qpainter)
        for animal in self.animals:
            animal.draw(qpainter)
        qpainter.end()
        self.updateAnimals()

    def __init__(self):
    
        super().__init__()

        self.top = window_top
        self.left = window_left
        self.height = window_height
        self.width = window_width
        self.title = window_title
        self.animals = []
        self.enviroment = classlib.Enviroment(env_size, env_size, tile_size)

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.show()

app = QtWidgets.QApplication([])

application = mywindow()

application.addAnimal(0,0,100)

sys.exit(app.exec())
