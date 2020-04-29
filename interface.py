import random
import sys
import threading

import pyqtgraph as pg
import numpy as np
import classeslib
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 600
WINDOW_TOP = 150
WINDOW_LEFT = 150
WINDOW_TITLE = "Evolution simulation"
CAMERA_SHIFT = 3
ENV_SIZE = 100
TILE_SIZE = 5
ANIMAL_SIZE = 10


class mywindow(QtWidgets.QMainWindow):  # Класс с основным окном
    def addAnimal(self, x, y, energy): # Функция, которая добавляет животное с заданными параметрами
        self.enviroment.addAnimal(x, y, 5, ANIMAL_SIZE, True)
        #self.update()

    def deleteAnimal(self, animal):  # Функция, которая удаляет животное, переданное в функцию
        self.enviroment.deleteAnimal(animal)
        # self.update()

    def paintEvent(self, event):
        self.UpdateGraph()
        qpainter = QPainter(self)
        self.enviroment.draw(qpainter, self.camera)  # Отрисовываем окр среду
        for animal in self.enviroment.animals:  # В этом цикле отрисовываются все животные
            animal.draw(qpainter, self.camera)
        for food in self.enviroment.foodList:  # В этом цикле отрисовываутся вся еда
            food.draw(qpainter, self.camera)
        qpainter.end()

    def keyPressEvent(self, event):
        camera_velosity = [0, 0]
        if event.key() == 32:  # 32 - Это пробел. Здесь если симуляция стояла на паузе, то запускается,
            if self.isActive:  # если нет - останавливается
                self.isActive = False
            else:
                self.isActive = True
        if event.key() == 87:  # 87 - это w. Здесь камера сдвигается вверх
            camera_velosity[1] -= CAMERA_SHIFT
        if event.key() == 83:  # 83 - это s. Здесь камера сдвигается вниз
            camera_velosity[1] += CAMERA_SHIFT
        if event.key() == 65:  # 65 - это a. Здесь камера сдвигается влево
            camera_velosity[0] -= CAMERA_SHIFT
        if event.key() == 68:  # 68 - это d. Здесь камера сдвигается вправо
            camera_velosity[0] += CAMERA_SHIFT
        self.camera.move(camera_velosity[0], camera_velosity[1])
        # self.repaint()

    def closeEvent(self, event):
        self.animalUpdateThread.stop()  # Перед выключением - подаем потоку сигнал выключиться

    def __init__(self):

        super().__init__()

        self.top = WINDOW_TOP
        self.left = WINDOW_LEFT
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        self.title = WINDOW_TITLE
        self.enviroment = classeslib.Enviroment(ENV_SIZE, ENV_SIZE, TILE_SIZE)  # Инициализируем окр среду
        self.camera = classeslib.Camera(0, 0)  # Инициализируем камеру
        self.isActive = True  # Запускаем симуляцию

        self.InitWindow()  # Инициализируем окно
        self.InitGraph()
        self.addAnimal(0, 0, 500)  # Создаем начальное животное
        self.addAnimal(100, 100, 500)
        for i in self.enviroment.animals:
            print(i.ID)

        self.animalUpdateThread = classeslib.AnimalUpdateThread(
            self)  # Инициализируем поток, который обрабатывает изменения
        self.animalUpdateThread.start()  # Запускаем поток

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.show()

    def InitGraph(self):
        title = "Population"
        self.plt = pg.plot()
        self.plt.setTitle(title)
        self.plt.setLabel('left', 'Value', units='V')
        self.plt.setLabel('bottom', 'Time', units='s')

    def UpdateGraph(self):
        self.animalUpdateThread.lock.acquire()
        y = self.enviroment.population
        c = self.plt.plot(range(0, len(y)), y, pen='r', name='main animal', clear=True)
        self.animalUpdateThread.lock.release()


app = QtWidgets.QApplication([])

application = mywindow()
if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
    pg.QtGui.QApplication.exec_()

sys.exit(app.exec())