class Tile:

    def __init__(self, ID, x, y):
        self.ID = ID
        self.x = x
        self.y = y
    

class Enviroment:

    def __init__(self, width, height):
        self.Tiles = [None] * width * height
        for i in range(width * height):
            self.Tiles[i] = Tile(i, int(i / width), i % width)

myEnv = Enviroment(10,10)

class Animal:
    def __init__(self,x,y,energy):
        self.x = x            
        self.y = y
        self.energy = energy
