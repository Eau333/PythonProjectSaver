import enum
import random
import time
import tkinter
from tkinter import simpledialog
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
        self.root = tkinter.Tk()
        self.root.eval(f'tk::PlaceWindow {self.root._w} center')
        self.root.withdraw()
        self.graphics = uno_gfx_api.unoGfx()
        self.graphics.set_welcome_message(welcome_message='Welcome to PyUno!')
        self.graphics.choose_num_players()
        self.gfx_updater = graphicsUpdater(unogame=self)
        self.playerCount = self.graphics.get_num_cpu()+1
        self.deck = deck()
        self.discardPile = []
        self.players = []
        for i in range(0, self.playerCount):
            self.players.append(player())
        self.currentTurn = 0
        self.order = 1
        self.activeCard = []
        self.active_colour = colour.wild
        self.graphics.set_card_counts(total_cards=len(self.deck.DrawPile), cards_per_player=7)
        self.graphics.main_setup()
        self.deal()
        self.gfx_updater.updateActiveCard()
        self.gfx_updater.showPlayerHand()
        self.roundover = False
        self.card_played_question_mark = False
        self.extra_draw_count = 0
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
        while not self.roundover:
            self.card_played_question_mark = False
            if self.currentTurn == 0:
                self.playerTurn()
            else:
                self.cpuTurn()
            if self.card_played_question_mark:
                self.checkActionCard()
            self.changeTurn()
            self.drawExtraCards()

    def playerTurn(self):
        self.graphics.player_hand.toggle_highlight()
        self.graphics.set_message("It is your turn.")
        self.graphics.update_window()

        if not self.checkPlayable(self.players[self.currentTurn].hand):
            self.graphics.set_message("You do not have any legal cards. You drew: "+self.drawCard(self.players[self.currentTurn].hand))
            drawn_card = self.players[self.currentTurn].hand[-1]
            self.graphics.player_hand.add_player_card(drawn_card.colour.name, drawn_card.action.name, drawn_card.number)
            self.graphics.update_window()
            time.sleep(2)

        if self.checkPlayable(self.players[self.currentTurn].hand):
            legal_card = False
            while not legal_card:
                selected_card = self.graphics.read_player_move()
                if self.checkLegal(self.players[0].hand[selected_card]):
                    legal_card = True
                    self.card_played_question_mark = True
                    if self.players[0].hand[selected_card].colour == colour.wild:
                        self.active_colour = self.inputColour()
                    self.makeActive(self.players[0].hand,selected_card)
                    self.gfx_updater.updateActiveCard()
                    self.graphics.player_hand.remove_card_index(selected_card)
                else:
                    self.graphics.set_message("Card played is not legal. Please choose a legal card.")
                self.graphics.update_window()

        self.graphics.player_hand.toggle_highlight()

    def cpuTurn(self):
        self.graphics.cpu_list[self.currentTurn-1].toggle_highlight()
        self.graphics.set_message("It\'s CPU "+str(self.currentTurn)+"\'s turn.")
        self.graphics.update_window()
        time.sleep(2)
        if not self.checkPlayable(self.players[self.currentTurn].hand):
            self.graphics.set_message(
                "CPU does not have any legal cards. CPU drew 1 card. ")
            self.drawCard(self.players[self.currentTurn].hand)
            self.graphics.cpu_list[self.currentTurn - 1].card_count += 1
            self.graphics.update_window()
            time.sleep(2)
        if self.checkPlayable(self.players[self.currentTurn].hand):
            self.cpuPlayCard()
        self.graphics.cpu_list[self.currentTurn-1].toggle_highlight()
        self.graphics.update_window()

    def checkLegal(self,checkCard):
        activeCard = self.activeCard[0]
        if checkCard.colour == activeCard.colour:
            return True
        elif activeCard.colour == colour.wild and checkCard.colour == self.active_colour:
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
            self.graphics.active_pile.discard_pile_size = 0
        self.moveCard(self.deck.DrawPile,drawHand,0)
        self.graphics.set_draw_pile_size(len(self.deck.DrawPile))
        self.graphics.update_window()
        return drawHand[-1].cardInfo()

    def inputColour(self):
        prompt = "Enter a colour:"
        while True:
            selected_colour = simpledialog.askstring(title="You played a wild card.",
                                                     prompt=prompt,
                                                     parent=self.root)
            if selected_colour == "blue":
                return colour.blue
            elif selected_colour == "green":
                return colour.green
            elif selected_colour == "red":
                return colour.red
            elif selected_colour == "yellow":
                return colour.yellow
            prompt = "Invalid colour. Please pick blue, green, red, or yellow."

    def changeTurn(self):
        self.currentTurn += self.order
        if self.currentTurn == -1:
            self.currentTurn = self.playerCount-1
        if self.currentTurn > self.playerCount-1:
            self.currentTurn = 0

    def cpuPlayCard(self):
        for cardIndex, card in enumerate(self.players[self.currentTurn].hand):
            if self.checkLegal(card):
                wild_message = ""
                if card.colour == colour.wild:
                    random_colour = random.choice([colour.blue, colour.green, colour.red, colour.yellow])
                    self.active_colour = random_colour
                    wild_message = ". Wild colour is "+random_colour.name
                self.makeActive(self.players[self.currentTurn].hand, cardIndex)
                self.card_played_question_mark = True
                self.gfx_updater.updateActiveCard()
                self.graphics.cpu_list[self.currentTurn - 1].card_count -= 1
                self.graphics.set_message("CPU played: "+card.cardInfo()+wild_message)
                self.graphics.update_window()
                time.sleep(2)
                return

    def checkActionCard(self):
        self.extra_draw_count = 0
        if self.activeCard[0].action == action.Skip:
            self.changeTurn()
        elif self.activeCard[0].action == action.Reverse:
            if self.playerCount == 2:
                self.changeTurn()
            else:
                self.order *= -1
        elif self.activeCard[0].action == action.Draw2:
            self.extra_draw_count = 2
        elif self.activeCard[0].action == action.Draw4:
            self.extra_draw_count = 4

    def drawExtraCards(self):
        if self.extra_draw_count > 0:
            for i in range(0, self.extra_draw_count):
                self.drawCard(self.players[self.currentTurn].hand)
                if self.currentTurn == 0:
                    drawn_card = self.players[0].hand[-1]
                    self.graphics.player_hand.add_player_card(drawn_card.colour.name, drawn_card.action.name,
                                                              drawn_card.number)
            if self.currentTurn == 0:
                self.graphics.set_message("You drew "+str(self.extra_draw_count)+" cards because a draw card was played.")
            else:
                self.graphics.set_message("CPU drew "+str(self.extra_draw_count)+" cards because a draw card was played.")
                self.graphics.cpu_list[self.currentTurn - 1].card_count += self.extra_draw_count
            self.graphics.update_window()
            time.sleep(2)
            self.changeTurn()
        self.extra_draw_count = 0


class graphicsUpdater():
    def __init__(self, unogame: game):
        self.unogame = unogame

    def updateActiveCard(self):
        colour = self.unogame.activeCard[0].colour
        action = self.unogame.activeCard[0].action
        number = self.unogame.activeCard[0].number
        self.unogame.graphics.set_active_card(colour.name,action.name,number)
        self.unogame.graphics.active_pile.discard_pile_size = len(self.unogame.discardPile)

    def showPlayerHand(self):
        for card in self.unogame.players[0].hand:
            self.unogame.graphics.player_hand.add_player_card(card.colour.name,card.action.name,card.number)
