import enum


class space(enum.Enum):
    empty = 1
    x = 2
    o = 3


def MakeBoard():
    board = []
    for i in range(1, 4):
        board.append([space.empty, space.empty, space.empty])
    return board


class TTTboard():
    def __init__(self):
        self.moves = 0
        self.board = MakeBoard()
        self._turn = space.x
        self.gameover = False
        self.dict = {
            space.empty: "   ",
            space.x: " x ",
            space.o: " o "
        }

    def changeturn(self):
        if self._turn == space.x:
            self._turn = space.o
        else:
            self._turn = space.x

    def print(self):
        for i in range(0, 3):
            print(self.dict[self.board[i][0]]+"|"+self.dict[self.board[i][1]]+"|"+self.dict[self.board[i][2]])
            if i < 2:
                print("---+---+---")


    def __input(self):
        row = int(input("Enter a row from 1 to 3:"))
        column = int(input("Enter a column from 1 to 3:"))
        self.__move(row, column)

    def __move(self, row, column):
        if self.board[(row - 1)][(column - 1)] == space.empty:
            self.board[(row - 1)][(column - 1)] = self._turn
            self.print()
            self.moves += 1
            self.changeturn()
        else:
            print("Space already in use. Please enter another move.")
            self.__input()

    def start(self):
        self.gameover = False
        while not self.gameover:
            self.__input()
            self.checkifover()
            if self.gameover:
                if input("Do you want to play again? Y/N").capitalize() == "Y":
                    self.restart()

    def checkifover(self):
        for i in range(0,3):
            #check row i
            if (self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2] and
                not self.board[i][1] == space.empty):
                    self.checkwinner(self.board[i][0])
            #check column i
            if (self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and
                not self.board[1][i] == space.empty):
                    self.checkwinner(self.board[0][i])
        #check diagonal 1
        if (self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and
            not self.board[1][1] == space.empty):
                self.checkwinner(self.board[1][1])
        #check diagonal 2
        if (self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and
            not self.board[1][1] == space.empty):
                self.checkwinner(self.board[1][1])
        if self.moves == 9:
            print("It's a tie.")
            self.gameover = True

    def checkwinner(self,winner):
        print("The winner is "+self.dict[winner])
        self.gameover = True

    def restart(self):
        self._turn = space.x
        self.moves = 0
        self.board = MakeBoard()
        self.gameover = False
        self.print()
