from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt

import threading 
import random
import time
import math

turn_delay = 0.15
food_size = 10

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.green)
        qpainter.setBrush(brush)
        qpainter.drawEllipse(self.x - camera.x, self.y - camera.y, food_size, food_size)

class Tile:

    def __init__(self, ID, x, y, size):
        self.ID = ID
        self.x = x
        self.y = y
        self.size = size

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.yellow)
        pen = QPen(Qt.yellow)
        qpainter.setPen(pen)
        qpainter.setBrush(brush)
        qpainter.drawRect(self.x - camera.x, self.y - camera.y, self.size, self.size)
    

class Enviroment:

    def __init__(self, width, height, tilesize):
        self.width = width
        self.height = height
        self.tilesize = tilesize
        self.Tiles = [None] * width * height
        self.foodList = []
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width) * tilesize, i % width * tilesize, tilesize)

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.yellow)
        pen = QPen(Qt.yellow)
        qpainter.setPen(pen)
        qpainter.setBrush(brush)
        qpainter.drawRect(- camera.x, - camera.y, self.height * self.tilesize, self.width * self.tilesize)
        

    def addFood(self, x, y):
        self.foodList.append(Food(x, y))

class Animal:
    def __init__(self,x,y,energy, speed, size, env):  
        self.x = x            
        self.y = y
        self.energy = energy
        self.speed = speed
        self.size = size
        self.env = env

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.blue)
        qpainter.setBrush(brush)
        yCoord = self.y - camera.y
        xCoord = self.x - camera.x
        qpainter.drawRect(xCoord, yCoord, self.size, self.size)

    def isDead(self):
        assert(self.energy > 0)

    def update(self):
        self.isDead()
        if self.env.foodList:
            foodDists = []
            for food in self.env.foodList:
                tmp = math.sqrt(abs(food.x - self.x)**2 + abs(food.y - self.y)**2)
                foodDists.append(tmp)
            food = self.env.foodList[foodDists.index(min(foodDists))]
            dist2food = min(foodDists)
            if dist2food <= self.speed:
                self.x,self.y = food.x,food.y
            else:
                targetTG = abs(food.y - self.y) / abs(food.x - self.x)
                x = self.speed / (targetTG + 1)
                y = x * targetTG
                self.x += x
                self.y += y

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
        self.isRunning = True

    def run(self):
        while self.isRunning:
            if (self.widget.isActive):
                self.lock.acquire()
                for animal in self.widget.animals:
                    try:
                        animal.update()
                    except AssertionError:
                        self.widget.deleteAnimal(animal)
                self.lock.release()
                time.sleep(turn_delay)
                self.widget.update()

    def stop(self):
        self.isRunning = False