# astroxii @ 2022
# Console Domino game

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.pieces = []

    def get_pieces(self) -> list:
        return self.pieces

    def set_pieces(self, pieces) -> None:
        self.pieces = pieces