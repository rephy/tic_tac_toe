from time import sleep
from os import system
import random

markers = ('X', 'O')

class Player:

    def __init__(self, board):
        self.score = 0
        self.board = board
        self.board.players.append(self)
        self.num = self.board.players.index(self) + 1
        self.marker = markers[self.num - 1]

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
            self.board.erase()
            self.board.display()
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

class Bot(Player):

    def __init__(self, board):
        super().__init__(board)

    def move(self):
        abc = ['A', 'B', 'C']

        rows, columns, diagonals = self.__check_opponent()
        if rows:
            row = list(rows[0].keys())[0]
            column = list(rows[0][row]).index('') + 1

            move = f'{row}{column}'
        elif columns:
            column = list(columns[0])[0]
            row = abc[list(columns[0])[1].index('')]

            move = f'{row}{column}'
        elif diagonals:
            possible_diagonals = [(-1, ['A3', 'B2', 'C1']), (1, ['A1', 'B2', 'C3'])]
            diagonal = list(diagonals[0])
            match_diagonal = possible_diagonals[0 if diagonal[0] == -1 else 1]

            move = match_diagonal[1][diagonal[1].index('')]
        else:
            move = f'{random.sample(abc, 1)[0]}{random.sample([1, 2, 3], 1)[0]}'

        while self.board.pos[abc.index(move[0])][int(move[1]) - 1] != '':
            move = f'{random.sample(abc, 1)[0]}{random.sample([1, 2, 3], 1)[0]}'

        self.board.pos[abc.index(move[0])][int(move[1]) - 1] = self.marker

        self.board.update_board()
        self.board.erase()
        self.board.display()

    def __check_opponent(self):
        rows = self.__check_opponent_rows()
        columns = self.__check_opponent_columns()
        diagonals = self.__check_opponent_diagonals()

        return rows, columns, diagonals

    def __check_opponent_rows(self):
        rows = []
        abc = ['A', 'B', 'C']
        for row in self.board.pos:
            if len([marker for marker in row if marker == markers[0]]) == 2 and [marker for marker in row if marker != markers[0]][0] == '':
                rows.append({abc[self.board.pos.index(row)]: row})
                print({abc[self.board.pos.index(row)]: row})
        return rows

    def __check_opponent_columns(self):
        columns = []
        for column_num in range(3):
            column = []
            for row in self.board.pos:
                column.append(row[column_num])
            if len([marker for marker in column if marker == markers[0]]) == 2 and [marker for marker in column if marker != markers[0]][0] == '':
                columns.append((column_num + 1, column))
        return columns

    def __check_opponent_diagonals(self):
        diagonals = []
        for diagonal_num in range(-1, 2, 2):
            pos = self.board.pos
            if diagonal_num == -1:
                diagonal = [pos[0][2], pos[1][1], pos[2][0]]
            else:
                diagonal = [pos[0][0], pos[1][1], pos[2][2]]

            if len([marker for marker in diagonal if marker == markers[0]]) == 2 and [marker for marker in diagonal if marker != markers[0]][0] == '':
                diagonals.append((diagonal_num, diagonal))

        return diagonals