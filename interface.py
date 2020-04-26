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
WINDOW_TITLE = "Evolution simulation"
CAMERA_SHIFT = 30
ENV_SIZE = 100
TILE_SIZE = 5
ANIMAL_SIZE = 10

class mywindow(QtWidgets.QMainWindow): # Класс с основным окном

    def addAnimal(self, x, y, energy, size): # Функция, которая добавляет животное с заданными параметрами
        self.enviroment.addAnimal(x, y, energy, size)
        self.update()

    def deleteAnimal(self, animal): # Функция, которая удаляет животное, переданное в функцию
        self.enviroment.deleteAnimal(animal)
        self.update()

    def paintEvent(self, event):
        qpainter = QPainter(self)
        self.enviroment.draw(qpainter, self.camera) # Отрисовываем окр среду
        for animal in self.enviroment.animals: # В этом цикле отрисовываются все животные
            animal.draw(qpainter, self.camera)
        for food in self.enviroment.foodList: # В этом цикле отрисовываутся вся еда
            food.draw(qpainter, self.camera)
        qpainter.end()

    def keyPressEvent(self, event):
        camera_velosity = [0, 0]
        if event.key() == 32: # 32 - Это пробел. Здесь если симуляция стояла на паузе, то запускается,
            if self.isActive: # если нет - останавливается
                self.isActive = False
            else:
                self.isActive = True
        if event.key() == 87: # 87 - это w. Здесь камера сдвигается вверх
            camera_velosity[1] -= CAMERA_SHIFT
        if event.key() == 83: # 83 - это s. Здесь камера сдвигается вниз
            camera_velosity[1] += CAMERA_SHIFT
        if event.key() == 65: # 65 - это a. Здесь камера сдвигается влево
            camera_velosity[0] -= CAMERA_SHIFT
        if event.key() == 68: # 68 - это d. Здесь камера сдвигается вправо
            camera_velosity[0] += CAMERA_SHIFT
        self.camera.move(camera_velosity[0], camera_velosity[1])
        self.repaint()

    def closeEvent(self, event):
        self.animalUpdateThread.stop() # Перед выключением - подаем потоку сигнал выключиться

    def __init__(self):

        super().__init__()

        self.top = WINDOW_TOP
        self.left = WINDOW_LEFT
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        self.title = WINDOW_TITLE
        self.enviroment = classlib.Enviroment(ENV_SIZE, ENV_SIZE, TILE_SIZE) # Инициализируем окр среду
        self.camera = classlib.Camera(0, 0) # Инициализируем камеру
        self.isActive = True # Запускаем симуляцию

        self.InitWindow() # Инициализируем окно

        self.addAnimal(100, 0, 500,12)  # Создаем начальное животное
        self.addAnimal(0, 0, 500,14)

        self.animalUpdateThread = classlib.AnimalUpdateThread(self) # Инициализируем поток, который обрабатывает изменения 
        self.animalUpdateThread.start() # Запускаем поток

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.show()

app = QtWidgets.QApplication([])

application = mywindow()

#print(len(application.enviroment.animals))

sys.exit(app.exec())
