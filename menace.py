import random
from random import choice
from collections import Counter
import json


class Menace:

    def __init__(self):
        self.board = [" "]*9
        self.beads = [10]*9
        # self.matchboxes = {}
        self.movesplayed = []
        try:
            a_file = open("data.json", "r")
            # output = a_file.read()
            self.matchboxes = json.loads(a_file.read())
        except:
            self.matchboxes = {}
            # print("No Pre Game exist")

    def printBoard(self):
        print("\nPositions:")
        print("0 | 1 | 2   ", self.board[0],
              "|", self.board[1], "|", self.board[2])
        print("--+---+--    --+---+--")
        print("3 | 4 | 5   ", self.board[3],
              "|", self.board[4], "|", self.board[5])
        print("--+---+--    --+---+--")
        print("6 | 7 | 8   ", self.board[6],
              "|", self.board[7], "|", self.board[8])
        print("\n")

    def userChance(self):
        pos = int(input("Enter position: "))
        if self.board[pos] != " ":
            print("Wrong input enter again")
            self.userChance()
        else:
            self.board[pos] = "X"

    def compChance(self):
        current_board = self.board_string()
        if current_board not in self.matchboxes:
            # If there is no matchbox for the current board state,
            # select a random move
            bead = random.choice([i for i, mark in enumerate(self.board) if mark == " "])
        else:
            current_beads = self.matchboxes[current_board]
            if len(current_beads):
                bead = random.choice(current_beads)
            else:
                # If there are no beads left in the matchbox for the current
                # board state, select a random move
                bead = random.choice([i for i, mark in enumerate(self.board) if mark == " "])
        self.board[bead] = "O"
        return bead


    def winning(self):
        winning_combos = [
            [0, 1, 2], [0, 3, 6], [0, 4, 8], # Rows and Diagonals starting from 0
            [1, 4, 7], [2, 4, 6], [2, 5, 8], # Columns and Diagonal starting from 2
            [3, 4, 5], [6, 7, 8] # Rows and Column starting from 3 and 6
        ]

        for combo in winning_combos:
            if (self.board[combo[0]] != ' ' and
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                return True

        return False


    def Tie(self):
        c = Counter(self.board)
        for i in c:
            if (i == " "):
                return False
        return True

    def beadChange(self, n):
        if n == 3:
            for (board, bead) in self.movesplayed:
                self.matchboxes[board] += [bead] * 3
            # self.num_win += 1
        elif n == 2:
            for (board, bead) in self.movesplayed:
                self.matchboxes[board].append(bead)
        elif n == 1:
            # Lose, remove a bead
            for (board, bead) in self.movesplayed:
                matchbox = self.matchboxes[board]
                matchbox.remove(bead)


    def resetGame(self):
        self.board = [" "]*9
        self.movesplayed = []

    def board_string(self):
        return ''.join(self.board)

    def playGame(self):
        chance = 0
        while (True):
            chance += 1
            move = self.compChance()
            self.board[move] = "O"
            # if chance>=2:
            if self.winning():
                self.printBoard()
                self.beadChange(3)
                print("Computer Won")
                break
            if self.Tie():
                self.printBoard()
                self.beadChange(2)
                print("Game Tie")
                break
            self.printBoard()
            self.userChance()
            # if chance>=2:
            if self.winning():
                self.printBoard()
                self.beadChange(1)
                print("You Won")
                break

    def instructions(self):
        print("\n")
        print("###########################################################")
        print("Welcome to MENACE Tic Tac Toe")
        print("The computer will gradually learn from the matches")
        print("The difficulty will increase with more number of matches")
        print("You are X and the Computer is O")
        print("Start Playing!")
        print("###########################################################")
        print("\n")

    def exit(self):
        ans = input("\nDo you want to continue? Yes or No\n")
        if ans.lower() == "no":
            print("Thank you for playing!! \n")
            a_file = open("data.json", "w")
            json.dump(self.matchboxes, a_file)
            a_file.close()
            return True
        else:
            a_file = open("data.json", "w")
            json.dump(self.matchboxes, a_file)
            a_file.close()
            return False

    # def Play(self):


if __name__ == '__main__':
    stop = False
    M = Menace()
    while(not stop):
        M.instructions()
        # print("Current beads are: ", Menace.__init__.beads)
        M.playGame()
        # print("Current beads are: ", Menace.beads)
        stop = M.exit()
        M.resetGame()
