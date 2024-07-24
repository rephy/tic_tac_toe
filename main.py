from board import Board
from players import Player
from time import sleep

markers = ('X', 'O')

board = Board()

board.erase()

player1 = Player(board)
player2 = Player(board)

while True:
    board.display()

    while True:
        player1.move()
        if player1.check():
            print('Player 1 wins!')
            break

        player2.move()
        if player2.check():
            print('Player 2 wins!')
            break

    sleep(3)
    play_again = input('Play again? (leave blank if no)')
    if play_again.strip() == '':
        break
    board.reset()