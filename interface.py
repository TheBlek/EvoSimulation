import random
import sys
import classeslib as classlib

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 600
WINDOW_TOP = 150
WINDOW_LEFT = 150
WINDOW_LTITLE = "Evolution simulation"
CAMERA_SHIFT = 3
ENV_SIZE = 256
TILE_SIZE = 5
ANIMAL_SIZE = 10

class mywindow(QtWidgets.QMainWindow):

    def addAnimal(self, x, y, energy):
        self.animals.append(classlib.Animal(x,y,energy, 15, ANIMAL_SIZE, self.enviroment))
        self.update()

    def deleteAnimal(self, animal):
        self.animals.remove(animal)

    def spawnNewFood(self):
        self.enviroment.addFood()
        self.update()

    def paintEvent(self, event):
        qpainter = QPainter(self)
        self.enviroment.draw(qpainter, self.camera)
        for animal in self.animals:
            animal.draw(qpainter, self.camera)
        for food in self.enviroment.foodList:
            food.draw(qpainter, self.camera)
        qpainter.end()

    def keyPressEvent(self, event):
        camera_velosity = [0, 0]
        if event.key() == 32: # 32 - Это пробел. Здесь симуляция ставится на паузу
            self.isActive = False
        if event.key() == 87:
            camera_velosity[1] -= CAMERA_SHIFT
        if event.key() == 83:
            camera_velosity[1] += CAMERA_SHIFT
        if event.key() == 65:
            camera_velosity[0] -= CAMERA_SHIFT
        if event.key() == 68:
            camera_velosity[0] += CAMERA_SHIFT
        self.camera.move(camera_velosity[0], camera_velosity[1])
        self.repaint()
        # w - 87; a - 65; s - 83; d - 68;

    def keyReleaseEvent(self, event):
        if event.key() == 32: # 32 - Это пробел. Здесь симуляция снимается с паузы
            self.isActive = True
        self.update()

    def closeEvent(self, event):
        self.animalUpdateThread.stop()

    def __init__(self):

        super().__init__()

        self.top = WINDOW_TOP
        self.left = WINDOW_LEFT
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        self.title = WINDOW_LTITLE
        self.animals = []
        self.food = []
        self.enviroment = classlib.Enviroment(ENV_SIZE, ENV_SIZE, TILE_SIZE)
        self.camera = classlib.Camera(0, 0)
        self.isActive = True
        self.animalUpdateThread = classlib.AnimalUpdateThread(self)
        self.animalUpdateThread.start()

        self.InitWindow()
        self.spawnNewFood()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.show()

app = QtWidgets.QApplication([])

application = mywindow()

application.addAnimal(0, 0, 500)

sys.exit(app.exec())
