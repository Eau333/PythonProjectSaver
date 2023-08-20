import enum
import random
import uno_gfx_api

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

    def cardInfo(self):
        if self.action == action.Number:
            return str(self.colour.name)+" "+str(self.number)
        else:
            return str(self.colour.name)+" "+str(self.action.name)

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
    def __init__(self):
        self.graphics = uno_gfx_api.unoGfx()
        self.graphics.set_welcome_message(welcome_message='Welcome to PyUno!')
        self.graphics.choose_num_players()
        self.playerCount = self.graphics.get_num_cpu()+1
        self.deck = deck()
        self.discardPile = []
        self.players = []
        for i in range(0, playerCount):
            self.players.append(player())
        self.currentTurn = 0
        self.order = 1
        self.activeCard = []
        self.deal()
        self.roundover = False
        self.gameStart()

    def moveCard(self,fromDeck,toDeck,cardIndex):
        toDeck.append(fromDeck[cardIndex])
        del fromDeck[cardIndex]

    def deal(self):
        for currentPlayer in range(0,self.playerCount):
            for j in range(0,7):
                self.moveCard(self.deck.DrawPile,self.players[currentPlayer].hand,0)
        self.makeActive(self.deck.DrawPile,0)

    def makeActive(self,fromDeck,cardIndex):
        if len(self.activeCard) >= 1:
            self.moveCard(self.activeCard,self.discardPile,0)
        self.moveCard(fromDeck,self.activeCard,cardIndex)

    def gameStart(self):
        print("Welcome to PyUno!")
        print("You are playing against "+str(self.playerCount-1)+" CPUs.")
        while not self.roundover:
            print("The active card is: "+self.activeCard[0].cardInfo())
            if self.currentTurn == 0:
                self.playerTurn()
            else:
                self.cpuTurn()

    def playerTurn(self):
        print("It is your turn.")
        print("Your hand:")
        for i in range(0, len(self.players[self.currentTurn].hand)):
            print(self.players[self.currentTurn].hand[i].cardInfo())
        if not self.checkPlayable(self.players[self.currentTurn].hand):
            print("You do not have any legal cards. You drew: "+self.drawCard(self.players[self.currentTurn].hand))

    def checkLegal(self,checkCard):
        activeCard = self.activeCard[0]
        if checkCard.colour == activeCard.colour:
            return True
        elif checkCard.number == activeCard.number and not activeCard.number == -1:
            return True
        elif checkCard.action == activeCard.action and not activeCard.action == action.Number:
            return True
        elif checkCard.colour == colour.wild:
            return True
        else:
            return False

    def checkPlayable(self,hand):
        for card in hand:
            if self.checkLegal(card):
                return True
        return False

    def drawCard(self,drawHand):
        if len(self.deck.DrawPile) < 1:
            self.deck.DrawPile = self.discardPile
            self.discardPile = []
            self.deck.shuffle()
        self.moveCard(self.deck.DrawPile,drawHand,0)
        return drawHand[-1].cardInfo()

