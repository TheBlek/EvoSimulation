from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush
from PyQt5.QtCore import Qt

import threading 
import random
import time

turn_delay = 0.15
food_size = 10

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.green)
        qpainter.setBrush(brush)
        qpainter.drawRect(self.x - camera.x, self.y - camera.y, food_size, food_size)

class Tile:

    def __init__(self, ID, x, y, size):
        self.ID = ID
        self.x = x
        self.y = y
        self.size = size

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.yellow)
        qpainter.setBrush(brush)
        qpainter.drawRect(self.x - camera.x, self.y - camera.y, self.size, self.size)
    

class Enviroment:

    def __init__(self, width, height, tilesize):
        self.width = width
        self.height = height
        self.tilesize = tilesize
        self.Tiles = [None] * width * height
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width) * tilesize, i % width * tilesize, tilesize)

    def draw(self, qpaiter, camera):
        for tile in self.Tiles:
            tile.draw(qpaiter, camera)

class Animal:
    def __init__(self,x,y,energy, size, env):  
        self.x = x            
        self.y = y
        self.energy = energy
        self.size = size
        self.env = env

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.blue)
        qpainter.setBrush(brush)
        yCoord = self.y + self.env.tilesize/4 - camera.y
        xCoord = self.x + self.env.tilesize/4 - camera.x
        qpainter.drawRect(xCoord, yCoord, self.size, self.size)

    def update(self):
        if self.x + 1 < (self.env.height - 1) * self.env.tilesize:
            self.x = self.x + self.env.tilesize
            self.energy = self.energy - 1
        elif self.y + 1 < (self.env.width - 1) * self.env.tilesize:
            self.y = self.y + self.env.tilesize
            self.energy = self.energy - 1
        elif self.x - 1 > 0:
            self.x = self.x - self.env.tilesize
            self.energy = self.energy - 1
        elif self.y - 1 > 0:
            self.y = self.y - self.env.tilesize
            self.energy = self.energy - 1

class Camera():
    def __init__(self, width_of_vision, height_of_vision, x=0, y=0):
        self.x = 0
        self.y = 0
        self.width_of_vision = width_of_vision
        self.height_of_vision = height_of_vision

    def move(self, x, y):
        self.x += x
        self.y += y

class AnimalUpdateThread(threading.Thread):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.lock = threading.Lock()

    def run(self):
        while True:
            if (self.widget.isActive):
                self.lock.acquire()
                for animal in self.widget.animals:
                    animal.update()
                self.lock.release()
                time.sleep(turn_delay)
                self.widget.update()
