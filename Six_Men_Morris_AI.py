import copy
import random

class Move:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

def evaluation_board(board):
    

class AlphaBetaPruning():
    MYTURN = 0
    OPPONENTTURN = 1
    INF = 100000000
    INVALID = -1
    def __init__(self, board):
        self.game_board = board

    def search(self, board, max_depth, team, depth=1, boundary=(-AlphaBetaPruning.INF, AlphaBetaPruning.INF)):
        best_act = -1
        if max_depth == depth:
            val = evaluation_board(board)
            return best_act, val

        possible_act_list = board.get_possible_act_list()
        for possible_act in possible_act_list:
            new_board = copy.deepcopy(self.game_board)
            new_board.act_chess(possible_act)
            temp, new_board_val = search(new_board, max_depth, not team, depth+1, boundary)
            if new_board_val == self.INVALID:
                continue

            if team == self.MYTURN:
                if boundary[0] < new_board_val:
                    boundary[0] = new_board_val
                    best_act = possible_act
            else:
                if boundary[1] > new_board_val:
                    boundary[1] = new_board_val
                    best_act = possible_act
            if boundary[0] > boundary[1]:
                return best_act, self.INVALID
            elif boundary[0] == boundary[1]:
                return best_act, boundary[0]

        if team == self.MYTURN:
            return best_act, boundary[0]
        else:
            return best_act, boundary[1]