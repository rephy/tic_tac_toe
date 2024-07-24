from time import sleep
from os import system

players = []
markers = ('X', 'O')

class Player:

    def __init__(self, board):
        players.append(self)
        self.score = 0
        self.num = players.index(self) + 1
        self.marker = markers[self.num - 1]
        self.board = board

    def move(self):
        move = input(f'Player {self.num}, where do you want to make your move? Example: A2\n').strip().upper()
        legal_moves = []
        invalid_move = False
        abc = ['A', 'B', 'C']
        for i in range(3):
            for j in range(3):
                legal_moves.append(f'{abc[i]}{j + 1}')

        try:
            self.board.pos[abc.index(move[0])][int(move[1]) - 1]
        except IndexError:
            invalid_move = True
        except ValueError:
            invalid_move = True
        else:
            if self.board.pos[abc.index(move[0])][int(move[1]) - 1] != '':
                invalid_move = True

        if not invalid_move:
            self.board.pos[abc.index(move[0])][int(move[1]) - 1] = self.marker

            self.board.update_board()
            self.board.erase()
            self.board.display()
        else:
            self.__invalid_move()


    def check(self):
        if self.__check_rows() or self.__check_columns() or self.__check_diagonals():
            self.score += 1
            self.board.scores[self.num - 1] = self.score
            return True
        return False

    def __invalid_move(self):
        print('That\'s not a legal move.')
        sleep(5)
        system('clear')
        self.board.display()
        self.move()

    def __check_rows(self):
        for row in self.board.pos:
            if (row[0] == row[1] == row[2] == self.marker):
                return True

    def __check_columns(self):
        for column_num in range(3):
            column = []
            for row in self.board.pos:
                column.append(row[column_num])

            if (column[0] == column[1] == column[2] == self.marker):
                return True

    def __check_diagonals(self):
        for diagonal_num in range(-1, 2, 2):
            pos = self.board.pos
            if diagonal_num == -1:
                diagonal = [pos[0][2], pos[1][1], pos[2][0]]
            else:
                diagonal = [pos[0][0], pos[1][1], pos[2][2]]

            if (diagonal[0] == diagonal[1] == diagonal[2] == self.marker):
                return True