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
camera_shift = 3
env_size = 50
tile_size = window_width / env_size
animal_size = tile_size / 2

class mywindow(QtWidgets.QMainWindow):

    def addAnimal(self, x, y, energy):
        self.animals.append(classlib.Animal(x,y,energy, animal_size, self.enviroment))
        self.update()

    def paintEvent(self, event):
        qpainter = QPainter(self)
        self.enviroment.draw(qpainter, self.camera)
        for animal in self.animals:
            animal.draw(qpainter, self.camera)
        qpainter.end()

    def keyPressEvent(self, event):
        camera_velosity = [0, 0]
        if event.key() == 32: # 32 - Это пробел. Здесь симуляция ставится на паузу
            self.isActive = False
        if event.key() == 87:
            camera_velosity[1] -= camera_shift
        if event.key() == 83:
            camera_velosity[1] += camera_shift
        if event.key() == 65:
            camera_velosity[0] -= camera_shift
        if event.key() == 68:
            camera_velosity[0] += camera_shift
        self.camera.move(camera_velosity[0], camera_velosity[1])
        self.repaint()
        # w - 87; a - 65; s - 83; d - 68;

    def keyReleaseEvent(self, event):
        if event.key() == 32: # 32 - Это пробел. Здесь симуляция снимается с паузы
            self.isActive = True
        self.update()

    def __init__(self):
    
        super().__init__()

        self.top = window_top
        self.left = window_left
        self.height = window_height
        self.width = window_width
        self.title = window_title
        self.animals = []
        self.enviroment = classlib.Enviroment(env_size, env_size, tile_size)
        self.camera = classlib.Camera(0,0)
        self.isActive = True
        self.animalUpdateThread = classlib.AnimalUpdateThread(self)
        self.animalUpdateThread.start()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.show()

app = QtWidgets.QApplication([])

application = mywindow()

application.addAnimal(0,0,100)

sys.exit(app.exec())
