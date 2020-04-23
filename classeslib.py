from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt

import threading 
import random
import time
import math
import sys

turn_delay = 0
food_size = 10
ENERGY_PER_FOOD = 1000
START_ENERGY = 100
REPRODUCE_COST = 5000
BASIC_MUTATION_RATE = 0.1
FOOD_SPAWN_RATE = 0.1

def sign(num):
    return -1 if num < 0 else 1

def Dist2Point(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def Animal2FoodCollision(animal, food):
    if Dist2Point(animal.x, animal.y, food.x, food.y) < food_size:
        return True
    if Dist2Point(animal.x + animal.size, animal.y, food.x, food.y) < food_size:
        return True
    if Dist2Point(animal.x, animal.y + animal.size, food.x, food.y) < food_size:
        return True
    if Dist2Point(animal.x + animal.size, animal.y + animal.size, food.x, food.y) < food_size:
        return True
    return False

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
        self.animals.append(Animal(x, y, speed, size, self))

    def deleteAnimal(self, animal):
        self.animals.remove(animal)

    def addFood(self):
        xRand = random.randint(0, self.tilesize * self.width)
        yRand = random.randint(0, self.tilesize * self.height)
        self.foodList.append(Food(xRand, yRand))

    def deleteFood(self, food):
        self.foodList.remove(food)

class Animal:
    def __init__(self, x, y, speed, size, enviroment):  
        self.x = x            
        self.y = y
        self.energy = START_ENERGY * size
        self.speed = speed
        self.size = size
        self.enviroment = enviroment
        color = self.speed ** 6
        color = math.floor(color)
        color = color % 16711680
        color = hex(color).split('x')[-1]
        self.color = '#' + '0' * (6 - len(color)) + color

    def draw(self, qpainter, camera):
        brush = QBrush(QColor(self.color))
        qpainter.setBrush(brush)
        yCoord = self.y - camera.y
        xCoord = self.x - camera.x
        qpainter.drawRect(xCoord, yCoord, self.size, self.size)

    def isDead(self):
        assert(self.energy > 0)

    def update(self):
        self.isDead()
        if self.energy > REPRODUCE_COST * self.size + 300:
            self.reproduce()
        if self.enviroment.foodList:
            foodDists = []
            for food in self.enviroment.foodList:
                tmp = math.sqrt((food.x - self.x)**2 + (food.y - self.y)**2)
                foodDists.append(tmp)
            food = self.enviroment.foodList[foodDists.index(min(foodDists))]
            dist2food = min(foodDists)
            if dist2food <= self.speed:
                self.x,self.y = food.x,food.y
                self.energy -= dist2food * self.speed
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
                    self.y += self.speed * self.speed * self.size * sign(food.y - self.y)
        else:
            self.energy -= 0.5 * self.size

    def eat(self, food):
        self.energy += ENERGY_PER_FOOD
        self.enviroment.deleteFood(food)

    def reproduce(self):
        self.energy -= REPRODUCE_COST
        child_speed = self.speed
        child_size = self.size
        child_color = self.color
        if random.random() < BASIC_MUTATION_RATE:
            mutation_speed_grade = random.random()
            mutation_size_grade = random.random()
            if random.random() > 0.5:
                mutation_speed_grade += 1
            else:
                mutation_speed_grade = 1 - mutation_speed_grade
            if random.random() > 0.5:
                mutation_size_grade += 1
            else:
                mutation_size_grade = 1 - mutation_size_grade
            child_speed *= mutation_speed_grade
            child_size *=  mutation_size_grade
        child_speed = child_speed % 50
        if child_size < 5:
            child_size = 5
        self.enviroment.addAnimal(self.x + 1, self.y + 1, child_speed, child_size)

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
                    for food in self.widget.enviroment.foodList:
                        if Animal2FoodCollision(animal, food):
                            animal.eat(food)
                    try:
                        animal.update()
                    except AssertionError:
                        self.widget.enviroment.deleteAnimal(animal)
                for i in range(math.floor(FOOD_SPAWN_RATE)):
                    self.widget.spawnNewFood()
                if random.random() < FOOD_SPAWN_RATE:
                    self.widget.spawnNewFood()
                if len(self.widget.enviroment.animals) == 0:
                    print("They all are dead!")
                    self.stop()
                else:
                    print(len(self.widget.enviroment.animals), len(self.widget.enviroment.foodList))
                self.lock.release()
                self.widget.update()
                time.sleep(turn_delay)

    def stop(self):
        self.isRunning = False