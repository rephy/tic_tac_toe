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
except KeyboardInterrupt:
    board.erase()
    quit()

if players == 1:
    player2 = Bot(board)
else:
    player2 = Player(board)

current_player = 1

board.erase()

def check(player):
    if player.check():
        print('Player 1 wins!')
        return 'Win'

    if player.tie():
        print('This game is tied!')
        return 'Tie'

    return None

def next():
    try:
        next.player += 1
    except AttributeError:
        next.player = 1

    if next.player > 2:
        next.player -= 2

    if next.player == 1:
        return player1
    else:
        return player2

while True:
    board.display()

    while True:
        player = next()
        player.move()
        if check(player):
            break

    sleep(3)
    try:
        play_again = input('Play again? (leave blank if yes) ')
    except KeyboardInterrupt:
        board.erase()
        quit()
    if play_again.strip() != '':
        break
    board.reset()