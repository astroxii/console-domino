from random import randint
from domino.utils import *

# astroxii @ 2022
# Console Domino game

class Board:
    def __init__(self, players, pieces_range = 7) -> None:
        self.running = False
        self.players = players
        self.p_round = 0
        self.pieces = []
        self.played_pieces = []
        self.corners = (None, None)

        # Generate pieces
        for i in range(pieces_range):
            for j in range(pieces_range):
                if j >= i : self.pieces.append((i, j))
        
    
    def run(self) -> None:
        # Setup
        cls()
        self.set_running(True)
        self.distribute()
        self.p_round = randint(0, len(self.players)-1)

        self.mainloop()

    def mainloop(self) -> None:
        # Game loop
        while(self.running):
            self.paint()
            self.read_play()
            self.next_round()
            self.check_end()

    def paint(self) -> None:
        # Painting game to the console
        cls()

        print(f"Domino | {len(self.players)} players\n\n\n")

        if(self.corners[0] != None and self.corners[1] != None):
            print(" ".join([f"[ {p[0]} | {p[1]} ]" for p in self.played_pieces]), "\n")
            print(f"Corner 1: [ {self.corners[0]} ]")
            print(f"Corner 2: [ {self.corners[1]} ]\n\n\n")
        else: 
            print("\n\n\n\n\n\n")

        print(f"{self.players[self.p_round].name}'s pieces:")
        print(", ".join([f"{self.players[self.p_round].pieces.index(p)+1} = [ {p[0]} | {p[1]} ]" for p in self.players[self.p_round].pieces]))
    

    def read_play(self) -> None:
        def read() -> int:
            play = None
            while(not play):
                self.paint()
                print("Choose a piece to play: ")
                try:
                    play = int(input())
                    assert play <= len(self.players[self.p_round].pieces)
                except:
                    play = None
            return abs(play-1)
        
        # Check if the current players must pick extra pieces to play
        has_piece = False
        if(len(self.played_pieces) > 0):
            for p in self.players[self.p_round].pieces:
                if(p[0] in self.corners or p[1] in self.corners):
                    has_piece = True
                    break
            
            if(not has_piece):
                has_piece = self.pick_piece()
            
        if(has_piece or len(self.played_pieces) == 0):
            play = read()
            
            if(len(self.played_pieces) == 0):
                # Any piece at beggining
                self.played_pieces.append(self.players[self.p_round].pieces.pop(play))

            elif(len(self.played_pieces) >= 1):
                valid = False
                while(not valid):
                    if(self.players[self.p_round].pieces[play].count(self.corners[0]) == 0 and
                    self.players[self.p_round].pieces[play].count(self.corners[1]) == 0):
                        play = read()
                    else:
                        valid = True
                        break

                if(self.players[self.p_round].pieces[play].count(self.corners[0]) > 0):
                    self.played_pieces.insert(0, self.players[self.p_round].pieces.pop(play))
                else: 
                    self.played_pieces.append(self.players[self.p_round].pieces.pop(play))
            
            self.define_corners()

        else:
            # This need to be checked...
            self.next_round()
            
    
    def define_corners(self) -> None:
        # Defines which number are required to play
        if(len(self.played_pieces) == 1):
            self.corners = (self.played_pieces[0][0], self.played_pieces[0][1])
        elif(len(self.played_pieces) >= 2):
            a = self.played_pieces[0][0] if self.played_pieces[0][0] not in self.played_pieces[1] or self.played_pieces[0][0] == self.played_pieces[0][1] else self.played_pieces[0][1]
            b = self.played_pieces[len(self.played_pieces)-1][0] if self.played_pieces[len(self.played_pieces)-1][0] not in self.played_pieces[len(self.played_pieces)-2] or self.played_pieces[len(self.played_pieces)-1][0] == self.played_pieces[len(self.played_pieces)-1][1] else self.played_pieces[len(self.played_pieces)-1][1]
            self.corners = (a, b)
        

    def pick_piece(self) -> bool:
        def read() -> int:
            play = None
            while(not play):
                self.paint()
                print("Choose a piece from the board: ")
                print(", ".join([f"{i+1} = [ ? | ? ]" for i in range(len(self.pieces))]), "\n")
                try:
                    play = int(input())
                    assert play <= len(self.pieces)
                except:
                    play = None
            return abs(play-1)

        # Goes until the end of available pieces to check if the game may continue
        if(len(self.pieces) > 0):
            found = False
            while(not found and len(self.pieces) > 0):
                piece = read()
                if(self.pieces[piece][0] in self.corners or self.pieces[piece][1] in self.corners):
                    found = True
                
                self.players[self.p_round].pieces.append(self.pieces.pop(piece))
            return found
        else:
            return False
        

    def next_round(self) -> None:
        if(self.p_round < len(self.players)-1):
            self.set_p_round(self.p_round+1)
        else:
            self.set_p_round(0)

    def check_end(self) -> None:
        # Win
        for p in self.players:
            if(len(p.pieces) == 0):
                cls()
                print("*****************************\n\n")
                print(f"Winner: {p.name}!")
                print("\n\n*****************************")
                self.set_running(False)
                # self.reset()
        
        # Tie
        blocked = True and len(self.pieces) == 0
        for pl in self.players:
            if(not blocked): break
            for pc in pl.pieces:
                if(pc[0] in self.corners or pc[1] in self.corners):
                    blocked = False
                    break

        if(blocked):
            cls()
            print("*****************************\n\n")
            print("Game blocked! Can't do anything from here.")
            print("Good game.")
            print("\n\n*****************************")
            self.set_running(False)

        

    def distribute(self) -> None:
        # Shuffle pieces
        for i in range(len(self.pieces)):
            tmp = self.pieces[i]

            idex = randint(0, len(self.pieces)-1) 
            while(idex == i): idex = randint(0, len(self.pieces)-1)

            self.pieces[i] = self.pieces[idex]
            self.pieces[idex] = tmp

        # 7 for each player
        for p in self.players:
            p.set_pieces([self.pieces.pop(0) for _ in range(7)])

    
    def set_running(self, running):
        self.running = running

    def set_p_round(self, p_round):
        self.p_round = p_round
