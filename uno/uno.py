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
    def __init__(self,colour,action,points,number = -1):
        self.colour = colour
        self.action = action
        self.number = number
        self.points = points

class deck():
    def __init__(self):
        self.DrawPile = []
        for c in colour:
            if not c == colour.wild:
                for n in range(0,10):
                    self.DrawPile.append(cards(c,action.Number,n,n))
                self.DrawPile.append(cards(c, action.Draw2,20))
                self.DrawPile.append(cards(c, action.Reverse,20))
                self.DrawPile.append(cards(c, action.Skip,20))
            else:
                self.DrawPile.append(cards(c, action.Wild,50))
                self.DrawPile.append(cards(c, action.Draw4,50))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.DrawPile)

class player():
    def __init__(self):
        self.hand = []
        self.points = 0

class game():
    def __init__(self,playerCount):
        self.playerCount = playerCount
        self.deck = deck()
        self.discardPile = []
        self.players = []
        for i in range(0, playerCount):
            self.players.append(player())
        self.currentTurn = 0
        self.order = 1
        self.activeCard = None
