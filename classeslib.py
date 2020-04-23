from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt

import threading 
import random
import time
import math

turn_delay = 0.05
food_size = 10
ENERGY_PER_FOOD = 1000
START_ENERGY = 1000
REPRODUCE_COST = 5000

def sign(num):
    return -1 if num < 0 else 1

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
        self.animals =[]
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width) * tilesize, i % width * tilesize, tilesize)

    def draw(self, qpainter, camera):
        brush = QBrush(Qt.yellow)
        pen = QPen(Qt.yellow)
        qpainter.setPen(pen)
        qpainter.setBrush(brush)
        qpainter.drawRect(- camera.x, - camera.y, self.height * self.tilesize, self.width * self.tilesize)
    
    def addAnimal(self, x, y, speed, size):
        self.animals.append(Animal(x, y, START_ENERGY, speed, size, self))

    def deleteAnimal(self, animal):
        self.animals.remove(animal)

    def addFood(self):
        xRand = random.randint(0, self.tilesize * self.width)
        yRand = random.randint(0, self.tilesize * self.height)
        self.foodList.append(Food(xRand, yRand))

    def deleteFood(self, food):
        self.foodList.remove(food)
        for i in range(random.randint(1, 2)):
            self.addFood()

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
        if self.energy > 6000:
            self.reproduce()
        if self.env.foodList:
            foodDists = []
            for food in self.env.foodList:
                tmp = math.sqrt((food.x - self.x)**2 + (food.y - self.y)**2)
                foodDists.append(tmp)
            food = self.env.foodList[foodDists.index(min(foodDists))]
            dist2food = min(foodDists)
            if dist2food <= self.speed:
                self.x,self.y = food.x,food.y
                self.energy -= dist2food
                self.eat(food)
            else:
                if food.x - self.x != 0 and food.y - self.y != 0:
                    targetTG = abs(food.y - self.y) / abs(food.x - self.x)
                    x = self.speed / math.sqrt(targetTG ** 2 + 1)
                    y = x * targetTG
                    x *= sign(food.x - self.x)
                    y *= sign(food.y - self.y)
                    self.x += x
                    self.y += y
                    self.energy -= self.speed
                else:
                    self.y += self.speed * sign(food.y - self.y)

    def eat(self, food):
        self.energy += ENERGY_PER_FOOD
        self.env.deleteFood(food)

    def reproduce(self):
        self.energy -= REPRODUCE_COST
        self.env.addAnimal(self.x, self.y, self.speed, self.size)

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
                for animal in self.widget.enviroment.animals:
                    try:
                        animal.update()
                    except AssertionError:
                        self.widget.enviroment.deleteAnimal(animal)
                self.lock.release()
                time.sleep(turn_delay)
                self.widget.update()

    def stop(self):
        self.isRunning = False