import Othello
import copy
import random

PLAYER1 = 1
PLAYER2 = 2


BOARD_VALUE = [
    [10, -5, 6, 3, 3, 6, -5, 10],
    [-5, -5, -5, -5, -5, -5, -5, -5],
    [6, -5, 4, 4, 4, 4, -5, 6],
    [3, -5, 4, 1, 1, 4, -5, 3],
    [3, -5, 4, 1, 1, 4, -5, 3],
    [6, -5, 4, 4, 4, 4, -5, 6],
    [-5, -5, -5, -5, -5, -5, -5, -5],
    [10, -5, 6, 3, 3, 6, -5, 10]]


class Move:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos


def changeplayer(turn):
    if turn == PLAYER1:
        return PLAYER2
    return PLAYER1


def nubmerLegalMove(board, neighbor, color):
    return len(Othello.legal_moves(board, neighbor, color))


def evaluation_move(board, x, y):
    return BOARD_VALUE[y][x]


def number_chess(color, white, black):
    if color == 1:
        return white - black
    return black - white


def find_max(board, max_depth, depth=1, alpha_beta=None):
    if alpha_beta is None:
        alpha_beta = []

    if len(board.probableMove) == 0:
        return []

    for x, y in board.probableMove:
        value = evaluation_move(board, x, y)
        copped_board = copy.deepcopy(board)
        copped_board.flip_chess(x, y)
        copped_board.chess += 1
        copped_board.changeplayer()
        copped_board.countLegalMoves()

        if copped_board.chess == 64:
            return (Move(1000, (x, y)), )

        if depth == max_depth:
            alpha_beta.append(Move(value, (x, y)))
        else:
            next_moves = find_max(copped_board, max_depth, depth + 1)
            if next_moves != []:
                next_move = random.choice(next_moves)
                alpha_beta.append(Move(value - next_move.value, (x, y)))
            else:
                alpha_beta.append(Move(value, (x, y)))

    biggest_move = []
    biggest = -1000
    for move in alpha_beta:
        if move.value > biggest:
            biggest = move.value
            biggest_move.clear()
            biggest_move.append(move)
        elif move.value == biggest:
            biggest_move.append(move)
    return biggest_move
