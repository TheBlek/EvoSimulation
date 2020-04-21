class Tile:
    ID

    def __init__(ID):
        self.ID = ID;
    
    


class Enviroment:
    Tiles[][] = [][]

    def __init__(width, height):
        for i in range(width):
            for j in range(height):
                self.Tiles[i][j] = Tile(height * (i - 1) + j)

myEnv = Enviroment(10,10)
print(Enviroment.Tiles[3][5])

