from prettytable import PrettyTable
from os import system

class Board(PrettyTable):

    def __init__(self):
        super().__init__()
        self.field_names = ['', '1', '2', '3']
        self.pos = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        self.players = []
        self.scores = [0, 0]
        self.update_board()

    def display(self):
        print(f'Player 1: {self.scores[0]} | {'Player 2' if type(self.players[1]).__name__ == 'Player' else 'Bot'}: {self.scores[1]}')

        print(self)

    def update_board(self):
        self.clear_rows()
        self.add_row(['A', self.pos[0][0], self.pos[0][1], self.pos[0][2]], divider=True)
        self.add_row(['B', self.pos[1][0], self.pos[1][1], self.pos[1][2]], divider=True)
        self.add_row(['C', self.pos[2][0], self.pos[2][1], self.pos[2][2]], divider=True)

    def erase(self):
        system('clear')

    def reset(self):
        self.pos = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]

        self.update_board()
        self.erase()