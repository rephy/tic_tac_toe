from board import Board
from players import Player, Bot
from time import sleep

markers = ('X', 'O')

board = Board()

board.erase()

player1 = Player(board)

try:
    players = int(input('One player or two player? (1 or 2) '))
except TypeError:
    players = 1

if players == 1:
    player2 = Bot(board)
else:
    player2 = Player(board)

board.erase()

def check(player):
    if player.check():
        print('Player 1 wins!')
        return 'Win'

    if player.tie():
        print('This game is tied!')
        return 'Tie'

    return None

while True:
    board.display()

    while True:
        player1.move()
        if check(player1):
            break

        player2.move()
        if check(player2):
            break

    sleep(3)
    play_again = input('Play again? (leave blank if yes) ')
    if play_again.strip() != '':
        break
    board.reset()