
class Position:
    def __init__(self, X: int, Y: int):
        self.x = X
        self.y = Y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x: int):
        self.x = x

    def setY(self, y: int):
        self.y = y
    def print(self):
        print(str(self.x) + " ," + str(self.y))
