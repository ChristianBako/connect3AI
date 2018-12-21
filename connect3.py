import random
import sys
import timeit

CONNECT = 3
COLS = 4
ROWS = 3
EMPTY = ' '
TIE = 'TIE'


class Connect3Board:

    def __init__(self, string=None):
        if string is not None:
            self.b = [list(line) for line in string.split('|')]
        else:
            self.b = [list(EMPTY * ROWS) for i in range(COLS)]

    def compact_string(self):
        return '|'.join([''.join(row) for row in self.b])

    def clone(self):
        return Connect3Board(self.compact_string())

    def get(self, i, j):
        return self.b[i][j] if i >= 0 and i < COLS and j >= 0 and j < ROWS else None

    def row(self, j):
        return [self.get(i, j) for i in range(COLS)]

    def col(self, i):
        return [self.get(i, j) for j in range(ROWS)]

    def put(self, i, j, val):
        self.b[i][j] = val
        return self

    def empties(self):
        return self.compact_string().count(EMPTY)

    def first_empty(self, i):
        j = ROWS - 1
        if self.get(i, j) != EMPTY:
            return None
        while j >= 0 and self.get(i, j) == EMPTY:
            j -= 1
        return j + 1

    def place(self, i, label):
        j = self.first_empty(i)
        if j is not None:
            self.put(i, j, label)
        return self

    def equals(self, board):
        return self.compact_string() == board.compact_string()

    def next(self, label):
        boards = []
        for i in range(COLS):
            j = self.first_empty(i)
            if j is not None:
                board = self.clone()
                board.put(i, j, label)
                boards.append(board)
        return boards

    def _winner_test(self, label, i, j, di, dj):
        for _ in range(CONNECT - 1):
            i += di
            j += dj
            if self.get(i, j) != label:
                return False
        return True

    def winner(self):
        for i in range(COLS):
            for j in range(ROWS):
                label = self.get(i, j)
                if label != EMPTY:
                    if self._winner_test(label, i, j, +1, 0) \
                            or self._winner_test(label, i, j, 0, +1) \
                            or self._winner_test(label, i, j, +1, +1) \
                            or self._winner_test(label, i, j, -1, +1):
                        return label
        return TIE if self.empties() == 0 else None

    def __str__(self):
        return stringify_boards([self])


def stringify_boards(boards):
    if len(boards) > 6:
        return stringify_boards(boards[0:6]) + '\n' + stringify_boards(boards[6:])
    else:
        s = ' '.join([' ' + ('-' * COLS) + ' '] * len(boards)) + '\n'
        for j in range(ROWS):
            rows = []
            for board in boards:
                rows.append('|' + ''.join(board.row(ROWS - 1 - j)) + '|')
            s += ' '.join(rows) + '\n'
        s += ' '.join([' ' + ('-' * COLS) + ' '] * len(boards))
        return s


class Game:
    def __init__(self, playerOne, playerTwo, board):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.board = board

    def checkendGame(self):
        if self.board.winner() is not None or self.board.winner() == TIE:
            return True
        return False

    ##Simple and abstract playgame method so each player can use whatever method they'd like to play the game.
    def playgame(self):
        self.playerOne.addBoardtoMemory(self.board)
        self.playerTwo.addBoardtoMemory(self.board)
        moves = [self.board]
        while not self.checkendGame():
            self.board = self.playerOne.makemove(self.board)
            moves.append(self.board)

            if self.checkendGame():
                break

            self.board = self.playerTwo.makemove(self.board)
            moves.append(self.board)
        print stringify_boards(moves)
        return self.board.winner()


##Abstract Class for our other players.
class Player(object):
    def __init__(self, playersymbol):
        self.playersymbol = playersymbol
        self.boardinBrain = []

    def getPlayerSymbol(self):
        return self.playersymbol

    def makemove(self, choices):
        pass

    def getCurrentBoard(self):
        return self.boardinBrain[-1]

    def addBoardtoMemory(self, board):
        self.boardinBrain.append(board)

    def getBoardsInBrain(self):
        return self.boardinBrain



##I'm not crazy about all the hardcoded "X"s and "O"s but since this is a limited implementaion, I did it to make it more readable.

class miniMaxPlayer(Player):
    def __init__(self, playersymbol):
        Player.__init__(self, playersymbol)

##  def findBlocks(self,board,symbol):
##      ##Attempted to find blocks for a symbol.
##      ##For example if XXO happens.
##      ##unnecessary since it's covered by others.
##      total = 0
##      for j in range(ROWS):
##          previous_symbol = ""
##          for x in board.row(j):
##              if x == symbol and x != previous_symbol and x != " ":
##                  total = total + 1
##              previous_symbol = x
##              total = 0
##
##      ##Check columns
##      for i in range(COLS):
##          previous_symbol = ""
##          for x in board.col(i):
##              if x == symbol and x != previous_symbol and x != " ":
##                  total = total + 1
##              previous_symbol = x
##      return total

    def findTwoInRow(self,board,symbol):
        total = 0
        for j in range(ROWS):
            previous2_symbol = ""
            previous_symbol = ""
            ##Checks if there are two in a row with or without a space in between.
            ##Does not account for if there is a platform for a piece to stand on.
            for x in board.row(j):
                if x == symbol and x == previous_symbol and previous2_symbol == " ":
                    total = total + 1
                elif x == symbol and previous_symbol == " " and x == previous2_symbol:
                    total = total + 1
                previous2_symbol = previous_symbol
                previous_symbol = x
        return total

    def findTwoInColumn(self,board,symbol):
        total = 0
        ##Check columns, and make sure there is space for another piece.
        for i in range(COLS):
            previous_symbol = " "
            previous2_symbol = " "

            for x in board.col(i):
                if x == symbol and x == previous_symbol and previous2_symbol == " ":
                    total = total + 1
                previous2_symbol = previous_symbol
                previous_symbol = x
        return total

    def findTwoInDiagnols(self,board,symbol):
        ##Diagnoal matching
        ##Hard coded, not my favorite solution.

        total = 0
        if board.get(1,1) == symbol or board.get(1,1) == " ":
            if board.get(0,0) == symbol or board.get(0,0) == " ":
                total = total + 1
            elif board.get(2,ROWS) == symbol or board.get(2,ROWS) == " ":
                total = total + 1
        if board.get(2,1) == symbol or board.get(2,1) == " ":
            if board.get(1,ROWS) == symbol or board.get(1,ROWS) == " ":
                total = total + 1
            elif board.get(COLS,ROWS) == symbol or board.get(COLS,ROWS) == " ":
                total =total + 1
        return total

    def computeHeuristic(self,board):
        ##Check for winning condition in row, check for winning cond in column
        ##Not going to be pretty
        total = 0

        ##Win conditions
        if board.winner() == "O":
            total = 400
        elif board.winner() == "X" or board.winner() == TIE:
            total = -400



        ##Check from trap conditions, combination or two pieces from opponent and for ourselves, if we can't find any then just compute singles.
        if self.findTwoInRow(board,"X") > 0 and self.findTwoInColumn(board,"X") > 0:
            total = total + (self.findTwoInRow(board,"X") + self.findTwoInColumn(board,"X") ) * -100
            total = total + self.findTwoInColumn(board,"X")*-30

        elif self.findTwoInRow(board,"X") > 0 and self.findTwoInDiagnols(board,"X") > 0:

            total = total + (self.findTwoInRow(board,"X") + self.findTwoInDiagnols(board,"X")) * -100
            total = total + self.findTwoInColumn(board,"X")*-30

        elif self.findTwoInColumn(board,"X") > 0 and self.findTwoInDiagnols(board,"X") > 0:
            total = total + (self.findTwoInColumn(board,"X") + self.findTwoInDiagnols(board,"X")) * -100
            total = total + self.findTwoInRow(board,"X")*-30

        else:
            total = total + self.findTwoInRow(board,"X")*-30
            total = total + self.findTwoInColumn(board,"X")*-30
            total = total + self.findTwoInDiagnols(board,"X")*-30

        if self.findTwoInRow(board,"O") > 0 and self.findTwoInColumn(board,"O") > 0:
            total = total + (self.findTwoInRow(board,"O") + self.findTwoInColumn(board,"O")) * 100
            total = total + self.findTwoInDiagnols(board,"O")*30
        elif self.findTwoInRow(board,"O") > 0 and self.findTwoInDiagnols(board,"O") > 0:
            total = total + (self.findTwoInRow(board,"O") + self.findTwoInDiagnols(board,"O")) * 100
            total = total + self.findTwoInColumn(board,"O")*30
        elif self.findTwoInColumn(board,"O") > 0 and self.findTwoInDiagnols(board,"O") > 0:
            total = total + (self.findTwoInColumn(board,"O") + self.findTwoInDiagnols(board,"O")) * 100
            total = total + self.findTwoInRow(board,"O")*30
        else:
            total = total + self.findTwoInRow(board,"O")*30
            total = total + self.findTwoInColumn(board,"O")*30
            total = total + self.findTwoInDiagnols(board,"O")*30
        return total

    ## USED FOR OLD IMPLEMENTATION
    ##def minLevel(self,boards):
    ##    min = 10000
    ##    minBoardChoice = None
    ##
    ##    for board in boards:
    ##        if self.computeHeuristic(board) <= min:
    ##            min = self.computeHeuristic(board)
    ##            minBoardChoice = board
    ##
    ##    print "MIN: " + str(min)
    ##    return [minBoardChoice,min]
    ##
    ##def maxLevel(self,boards):
    ##    max = -10000
    ##    maxboardChoice = None
    ##
    ##    for board in boards:
    ##        if self.computeHeuristic(board) >= max:
    ##            max = self.computeHeuristic(board)
    ##            maxboardChoice = board
    ##
    ##    if maxboardChoice == None:
    ##        raise Exception("BAD MAX BOARD")
    ##
    ##    print "MAX: " + str(max)
    ##    return [maxboardChoice,max]



    ##This function and AB pruning are the same, except AB checks each recursive call with a and b values to see if it should continue.
    ##Reurses in on itself and adds each layer onto the stack, switches between player and opponent for arbitrary depth.
    def minimax(self,depth,choices,playerSymbol):
        ##Old implementation.
        ##finalBoardValues = {}
        ##for maxboard in maxBoards:
        ##    level2 = []
        ##    for minboard in maxboard.next("X"):
        ##        level2.append(self.maxLevel(minboard.next("O"))[1]+self.computeHeuristic(minboard))
        ##    if len(level2) > 0:
        ##        finalBoardValues[min(level2)+ self.computeHeuristic(maxboard) ] = maxboard
        ##    else:
        ##        finalBoardValues[self.computeHeuristic(maxboard) ] = maxboard
        ##return finalBoardValues[max(finalBoardValues.keys())]

        if depth == 0 or choices.winner() is not None:
            return [board,self.computeHeuristic(choices)]

        if playerSymbol == "O":
            utility = [None,-10000]
            for choice in choices.next("O"):
                max = self.minimax(depth-1,choice,"X")
                if utility[1] < max[1]:
                    utility = [choice,max[1]]
            return utility

        elif playerSymbol == "X":
            utility = [None,10000]
            for choice in choices.next("X"):
                min = self.minimax(depth-1,choice,"O")
                if utility[1] > min[1]:
                    utility = [choice,min[1]]
            return utility


    ##Make move function is overriden from player to make it easy to play the game.
    def makemove(self, board):
        return self.minimax(5,board,"O")[0]


class AlphaBetaPlayer(miniMaxPlayer):
    def __init__(self, playersymbol):
        Player.__init__(self, playersymbol)
        miniMaxPlayer(Player)

    ##Effectively the same as MiniMax.

    def alphaBeta(self,depth,board,a,b,playerSymbol):
        if depth == 0 or board.winner() is not None:
            return [board,self.computeHeuristic(board)]

        if playerSymbol == "O":
            utility = [None,-10000]
            for choice in board.next("O"):
                maxBoard = self.alphaBeta(depth-1,choice,a,b,"X")
                if utility[1] < maxBoard[1]:
                    utility = [choice,maxBoard[1]]

                a = max(a,utility[1])
                if a > b:
                    break

            return utility

        elif playerSymbol == "X":
            utility= [None,10000]
            for choice in board.next("X"):
                minBoard = self.alphaBeta(depth-1,choice,a,b,"O")
                if utility[1] > minBoard[1]:
                    utility = [choice,minBoard[1]]

                b = min(b,utility[1])

                if a > b:
                    break
            return utility

    def makemove(self,board):
        return self.alphaBeta(5,board,-10000,10000,"O")[0]

class RandomPlayer(Player):
    def __init__(self, playersymbol):
        Player.__init__(self, playersymbol)

    ##Just computes the next board and randomly get's one.
    def makemove(self, curboard):
        random.seed()
        choices = curboard.next(self.getPlayerSymbol())
        for nextboard in choices:
            if random.randrange(1, 5) == 3:
                self.addBoardtoMemory(nextboard)
                return nextboard
        self.addBoardtoMemory(choices[0])
        return choices[0]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        board = Connect3Board(sys.argv[2] if len(sys.argv) > 2 else None)

        if cmd == 'print':
            print(board)
        elif cmd == 'random':
            randomPlayer1 = RandomPlayer("X")
            randomPlayer2 = RandomPlayer("O")
            game = Game(randomPlayer1, randomPlayer2, board)
            game.playgame()
        elif cmd == "minimax":
            randomPlayer1 = RandomPlayer("X")
            miniMaxPlayer = miniMaxPlayer("O")

            game = Game(randomPlayer1, miniMaxPlayer, board)
            game.playgame()

        elif cmd == "alphabeta":
            randomPlayer1 = RandomPlayer("X")
            alphaBetaPlayer = AlphaBetaPlayer("O")
            game = Game(randomPlayer1, alphaBetaPlayer, board)
            game.playgame()
