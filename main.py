from domino.board import Board
from domino.player import Player
from domino.utils import *

# astroxii @ 2022
# Console Domino game

def menu():
    choose = None
    while(not choose):
        cls()
        print("***********************\n")
        print("Welcome to Console Domino!\n\n")
        print("1 - Start")
        print("2 - Exit")
        print("\n*********************")
        try:
            choose = int(input())
            assert choose in [1, 2]
        except:
            cls()
            choose = None

    cls()

    if(choose == 1):
        # Setup
        n_players = None
        while(not n_players):
            print("Number of players (2, 3 or 4):")
            try:
                n_players = int(input())
                assert n_players in [2, 3, 4]
            except:
                cls()
                n_players = None

        names = []
        for i in range(n_players):
            print(f"Name of player #{i+1}:")
            names.append(str(input()))

        # Creates game board and starts
        board = Board([Player(name) for name in names])
        board.run()

    elif(choose == 2):
        exit(0)


if __name__ == "__main__":

    menu()
