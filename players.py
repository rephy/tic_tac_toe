from time import sleep
from os import system
import random

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

markers = ('X', 'O')

class Player:

    def __init__(self, board):
        self.score = 0
        self.board = board
        self.board.players.append(self)
        self.num = self.board.players.index(self) + 1
        self.marker = markers[self.num - 1]

    def move(self):
        try:
            move = input(f'Player {self.num}, where do you want to make your move? Example: A2\n').strip().upper()
        except KeyboardInterrupt:
            self.board.erase()
            quit()
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

    def tie(self):
        if not self.check():
            pos_list = []
            for row in self.board.pos:
                pos_list += row
            if '' not in pos_list:
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

        move = self.__defensive_move()
        possible_move, count = self.__offensive_move()
        if (move is None) or (count == 2):
            move = possible_move
            if move is None:
                move = random.sample(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], 1)[0]
                while self.board.pos[abc.index(move[0])][int(move[1]) - 1] != '':
                    move = random.sample(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], 1)[0]

        self.board.pos[abc.index(move[0])][int(move[1]) - 1] = self.marker

        self.board.update_board()
        self.board.erase()
        self.board.display()

    def __defensive_move(self):
        abc = ['A', 'B', 'C']

        rows, columns, diagonals = self.__check_opponent()
        move = ''
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

        return (move if move != '' else None)

    def __offensive_move(self):
        abc = ['A', 'B', 'C']

        rows, columns, diagonals = self.__check_free_places()
        possible_moves = []
        move = ''
        for a_row in rows:
            row = list(a_row.keys())[0]

            possible_moves.append(('row', row, a_row['count']))
        for a_column in columns:
            column = list(a_column)[0]

            possible_moves.append(('column', column, a_column[2]))
        for a_diagonal in diagonals:
            possible_diagonals = [(-1, ['A3', 'B2', 'C1']), (1, ['A1', 'B2', 'C3'])]
            diagonal = list(a_diagonal)
            match_diagonal = possible_diagonals[0 if diagonal[0] == -1 else 1]

            possible_moves.append(('diagonal', match_diagonal, diagonal[2]))

        if not (diagonals or columns or rows):
            return None, None

        counts = [possible_move[2] for possible_move in possible_moves]
        counts_max = max(counts)

        possible_moves = [possible_move for possible_move in possible_moves if possible_move[2] == counts_max]
        place = random.sample(possible_moves, 1)[0]

        if place[0] == 'row':
            move = f'{place[1]}{random.sample([1, 2, 3], 1)[0]}'
            while self.board.pos[abc.index(move[0])][int(move[1]) - 1] != '':
                move = f'{place[1]}{random.sample([1, 2, 3], 1)[0]}'
        elif place[0] == 'column':
            move = f'{random.sample(['A', 'B', 'C'], 1)[0]}{place[1]}'
            while self.board.pos[abc.index(move[0])][int(move[1]) - 1] != '':
                move = f'{random.sample(['A', 'B', 'C'], 1)[0]}{place[1]}'
        elif place[0] == 'diagonal':
            move = random.sample(place[1][0], 1)
            while self.board.pos[abc.index(move[0])][int(move[1]) - 1] != '':
                move = random.sample(place[1], 1)[0]

        return move, counts_max

    def __check_opponent(self):
        rows = self.__check_opponent_rows()
        columns = self.__check_opponent_columns()
        diagonals = self.__check_opponent_diagonals()

        return rows, columns, diagonals

    def __check_free_places(self):
        rows = self.__check_free_rows()
        columns = self.__check_free_columns()
        diagonals = self.__check_free_diagonals()

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

    def __check_free_rows(self):
        rows = []
        abc = ['A', 'B', 'C']
        for row in self.board.pos:
            if (row[0] != markers[0]) and (row[1] != markers[0]) and (row[2] != markers[0]):
                count = 0
                for value in row:
                    if value != '':
                        count += 1

                rows.append({abc[self.board.pos.index(row)]: row, 'count': count})
        return rows

    def __check_free_columns(self):
        columns = []
        for column_num in range(3):
            column = []
            for row in self.board.pos:
                column.append(row[column_num])
            if (column[0] != markers[0]) and (column[1] != markers[0]) and (column[2] != markers[0]):
                count = 0
                for value in column:
                    if value != '':
                        count += 1
                columns.append((column_num + 1, column, count))
        return columns

    def __check_free_diagonals(self):
        diagonals = []
        for diagonal_num in range(-1, 2, 2):
            pos = self.board.pos
            if diagonal_num == -1:
                diagonal = [pos[0][2], pos[1][1], pos[2][0]]
            else:
                diagonal = [pos[0][0], pos[1][1], pos[2][2]]

            if (diagonal[0] != markers[0]) and (diagonal[1] != markers[0]) and (diagonal[2] != markers[0]):
                count = 0
                for value in diagonal:
                    if value != '':
                        count += 1
                diagonals.append((diagonal_num, diagonal, count))

        return diagonals