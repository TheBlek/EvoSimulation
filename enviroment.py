class Tile:

    def __init__(self, ID, x, y):
        self.ID = ID
        self.x = x
        self.y = y
    

class Enviroment:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.Tiles = [None] * width * height
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width), i % width)

class Animal:
    def __init__(self,x,y,energy):
        self.x = x            
        self.y = y
        self.energy = energy

    def Do(self, env):
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

def update(animals, enviroment):
    for animal in animals:
        animal.Do(enviroment)

myEnv = Enviroment(10, 10)
myAnimal = Animal(0,0,100)
animals = [myAnimal]
while True:
    update(animals, myEnv)
    print(myAnimal.x, myAnimal.y, myAnimal.energy)