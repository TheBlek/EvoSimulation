import PyQt5
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
        self.Tiles = [None] * width * height
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width) * tilesize, i % width * tilesize, tilesize)
        

    def draw(self, qpaiter):
        for tile in self.Tiles:
            tile.draw(qpaiter)

class Animal:
    def __init__(self,x,y,energy):
        self.x = x            
        self.y = y
        self.energy = energy

    def draw(self, qpainter):
        pass

    def update(self, env):
        if self.x + 1 < env.height:
            self.x = self.x + 1
            self.energy = self.energy - 1
        elif self.y + 1 < env.width:
            self.y = self.y + 1
            self.energy = self.energy - 1
        elif self.x - 1 > 0:
            self.x = self.x - 1
            self.energy = self.energy - 1
        elif self.y - 1 > 0:
            self.y = self.y - 1
            self.energy = self.energy - 1
        