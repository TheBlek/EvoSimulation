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
BASIC_MUTATION_RATE = 0.05
FOOD_SPAWN_RATE = 0.1

def sign(num): # Функция возвращения знака числа. Если 0 - возвращает 1
    return -1 if num < 0 else 1

def Dist2Point(x1, y1, x2, y2): # Функция, которая возвращает расстояние между двумя точками по их координатам
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) # Использована простая теорема пифагора

def Animal2FoodCollision(animal, food): # Функция, которая обрабатывает есть ли столкновение между животным и едой 
    if Dist2Point(animal.x, animal.y, food.x, food.y) < food_size: # Проверяем расстояние от левого верхнего угла
        return True
    if Dist2Point(animal.x + animal.size, animal.y, food.x, food.y) < food_size: # Проверяем расстояние от правого верхнего угла
        return True
    if Dist2Point(animal.x, animal.y + animal.size, food.x, food.y) < food_size: # Проверяем расстояние от левого нижнего угла
        return True
    if Dist2Point(animal.x + animal.size, animal.y + animal.size, food.x, food.y) < food_size: # Проверяем расстояние от правого нижнего угла
        return True
    return False

class Food: # Класс еды
    def __init__(self, x, y): # При инициализации просит только координаты
        self.x = x
        self.y = y

    def draw(self, qpainter, camera): # Функция, отвечающая за рисование еды
        brush = QBrush(Qt.green)
        qpainter.setBrush(brush)
        qpainter.drawEllipse(self.x - camera.x, self.y - camera.y, food_size, food_size)

class Tile: # Класс клетки
    def __init__(self, ID, x, y, size): # На вход просит координаты, размер и id
        self.ID = ID
        self.x = x
        self.y = y
        self.size = size

    def draw(self, qpainter, camera): # Функция, отвечающая за рисование клетки, пока не изпользуется 
        brush = QBrush(Qt.yellow)
        pen = QPen(Qt.yellow)
        qpainter.setPen(pen)
        qpainter.setBrush(brush)
        qpainter.drawRect(self.x - camera.x, self.y - camera.y, self.size, self.size)
    

class Enviroment: # Класс окружающей среды
    def __init__(self, width, height, tilesize):
        self.width = width
        self.height = height
        self.tilesize = tilesize
        self.Tiles = [None] * width * height
        self.foodList = []
        self.animals =[]
        self.population = []
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width) * tilesize, i % width * tilesize, tilesize)

    def draw(self, qpainter, camera): # Функция, отвечающаа за рисование окружающей среды
        brush = QBrush(Qt.yellow)
        pen = QPen(Qt.yellow)
        qpainter.setPen(pen)
        qpainter.setBrush(brush) # Окр среда рисуется как один прямоугольник
        qpainter.drawRect(- camera.x, - camera.y, self.height * self.tilesize, self.width * self.tilesize)
    
    def addAnimal(self, x, y, speed, size, is_genderless): # Функция, которая добавляет в окр среду животное с переданными параметрами
        self.animals.append(Animal(x, y, speed, size, self, is_genderless))

    def deleteAnimal(self, animal): # Функция, которая удалает переданное животное из окр среды
        self.animals.remove(animal)

    def addFood(self): # Функция, которая добавляет еду в случайном месте с окр среде
        xRand = random.randint(0, self.tilesize * self.width)
        yRand = random.randint(0, self.tilesize * self.height)
        self.foodList.append(Food(xRand, yRand))

    def deleteFood(self, food): # Функция, которая удаляет из окр среды переданную еду 
        self.foodList.remove(food)

class Animal:
    def __init__(self, x, y, speed, size, enviroment, is_genderless):  
        self.x = x            
        self.y = y
        self.speed = speed
        self.size = size
        self.enviroment = enviroment
        self.vision_radius = 150
        self.is_genderless = is_genderless
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
            self.speed *= mutation_speed_grade
            self.size *=  mutation_size_grade
        self.speed = self.speed % 50
        if self.size < 5:
            self.size = 5
        if random.random() < BASIC_MUTATION_RATE:
            is_genderless = not is_genderless
        if not is_genderless:
            if random.random() < 0.5:
                self.is_male = True
            else:
                self.is_male = False
        self.ready_for_reproduce = False
        color = self.speed ** 6
        color = math.floor(color)
        color = color % 16711680
        color = hex(color).split('x')[-1]
        self.color = '#' + '0' * (6 - len(color)) + color
        self.energy = START_ENERGY * size

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
            if self.is_genderless:
                self.genderlessReproduce()
            else:
                self.genderReproduce()
        if self.enviroment.foodList:
            foodDists = []
            closestFood = self.enviroment.foodList[0]
            dist_to_closest_food = 10000000
            for food in self.enviroment.foodList:
                tmp = math.sqrt((food.x - self.x)**2 + (food.y - self.y)**2)
                if tmp < self.vision_radius and tmp < dist_to_closest_food:
                    closestFood = food
                    dist_to_closest_food = tmp
            if dist_to_closest_food <= self.speed:
                self.x,self.y = food.x,food.y
                self.energy -= dist_to_closest_food * self.speed
            elif dist_to_closest_food != 10000000:
                self.moveTo(closestFood.x, closestFood.y)
        else:
            self.energy -= self.size

    def eat(self, food):
        self.energy += ENERGY_PER_FOOD
        self.enviroment.deleteFood(food)

    def moveTo(self, x, y):
        if x != self.x:
            targetTG = abs(y - self.y) / abs(x - self.x)
            dx = self.speed / math.sqrt(targetTG ** 2 + 1)
            dy = dx * targetTG
            dx *= sign(x - self.x)
            dy *= sign(y - self.y)
            self.x += dx
            self.y += dy
            self.energy -= self.speed
        else:
            self.y += self.speed * self.speed * self.size * sign(y - self.y)

    def genderlessReproduce(self):
        self.energy -= REPRODUCE_COST * self.size
        self.enviroment.addAnimal(self.x + 5, self.y + 5, self.speed, self.size, True)

    def genderReproduce(self):
        if not self.is_male:
            self.ready_for_reproduce = True
        else:
            closest_partner = animals[0]
            dist_to_closest_partner = 10000000
            for animal in self.enviroment.animals:
                dist = Dist2Point(self.x, self.y, animal.x, animal.y)
                if not animal.is_male and animal.ready_for_reproduce and dist < dist_to_closest_partner:
                    closest_partner = animal
                    dist_to_closest_partner = dist
            if dist_to_closest_partner != 10000000:
                self.moveTo(closest_partner.x, closest_partner.y)
            if dist_to_closest_partner < 1:
                print("Making new animal")
                self.energy -= REPRODUCE_COST * self.size
                child_speed = (self.speed + closest_partner.speed) / 2
                child_size = (self.size + closest_partner.size) / 2
                self.addAnimal(self.x, self.y, child_speed, child_size, False)

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
                if len(self.widget.enviroment.animals) == 0:
                    self.stop()
                for animal in self.widget.enviroment.animals:
                    for food in self.widget.enviroment.foodList:
                        if Animal2FoodCollision(animal, food):
                            animal.eat(food)
                    try:
                        animal.update()
                    except AssertionError:
                        self.widget.enviroment.deleteAnimal(animal)
                for i in range(math.floor(FOOD_SPAWN_RATE)):
                    self.widget.enviroment.addFood()
                if random.random() < FOOD_SPAWN_RATE:
                    self.widget.enviroment.addFood()
                if self.widget.enviroment.population != len(self.widget.enviroment.animals):
                    self.widget.enviroment.population.append(len(self.widget.enviroment.animals))
                self.lock.release()
                self.widget.update()
                time.sleep(turn_delay)

    def stop(self):
        self.isRunning = False