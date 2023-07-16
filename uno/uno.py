import enum
import random

class colour(enum.Enum):
    blue = 1
    green = 2
    red = 3
    yellow = 4
    wild = 5

class action(enum.Enum):
    Draw2 = 1
    Reverse = 2
    Skip = 3
    Draw4 = 4
    Wild = 5
    Number = 6

class cards():
    def __init__(self,colour,action,number = -1):
        self.colour = colour
        self.action = action
        self.number = number

class deck():
    def __init__(self):
        self.DrawPile = []
        for c in colour:
            if not c == colour.wild:
                for n in range(0,10):
                    self.DrawPile.append(cards(c,action.Number,n))
                self.DrawPile.append(cards(c, action.Draw2))
                self.DrawPile.append(cards(c, action.Reverse))
                self.DrawPile.append(cards(c, action.Skip))
            else:
                self.DrawPile.append(cards(c, action.Wild))
                self.DrawPile.append(cards(c, action.Draw4))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.DrawPile)