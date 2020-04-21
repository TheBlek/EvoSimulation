from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush
from PyQt5.QtCore import Qt
import random

class Tile:

    def __init__(self, ID, x, y, size):
        self.ID = ID
        self.x = x
        self.y = y
        self.size = size

    def draw(self, qpainter):
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        brush = QBrush(Qt.yellow)
        qpainter.setBrush(brush)
        qpainter.drawRect(self.x, self.y, self.size, self.size)
    

class Enviroment:

    def __init__(self, width, height, tilesize):
        self.width = width
        self.height = height
        self.tilesize = tilesize
        self.Tiles = [None] * width * height
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width) * tilesize, i % width * tilesize, tilesize)

    def draw(self, qpaiter):
        for tile in self.Tiles:
            tile.draw(qpaiter)

class Animal:
    def __init__(self,x,y,energy, size, env):  
        self.x = x            
        self.y = y
        self.energy = energy
        self.size = size
        self.env = env

    def draw(self, qpainter):
        brush = QBrush(Qt.blue)
        qpainter.setBrush(brush)
        qpainter.drawRect(self.x + self.env.tilesize/4, self.y + self.env.tilesize/4, self.size, self.size)

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