import copy
import random

class Move:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos


class AlphaBetaPruning():
    MYTURN = 0
    OPPONENTTURN = 1
    INF = 100000000
    INVALID = -1

    # board value according to possible mill(x2) form and freeness(x1)
    BOARD_VALUE = [
        4+2, 2+3, 4+2,
        4+2, 2+3, 4+2,
        2+3, 2+3, 2+3, 2+3,
        4+2, 2+3, 4+2,
        4+2, 2+3, 4+2
    ]

    def __init__(self, board):
        self.game_board = board

    def evaluate_value_in(self, board, index):
        totalValue = 0
        for i in board.BESIDE_INDEX[index]:
            if board.get_chess_in(i) == board.EMPTY:
                totalValue += 2
        return totalValue

    def evaluate_mill_value(self, board, team):
        totalValue = 0
        VALUE_FOR_ONE_CHESS_REMAIN_TO_FORM_MILL = 10
        VALUE_SUCCESSFULLY_FORM_MILL = 80

        chess_on_board_list = [i for i in range(16) if board.get_chess_in(i) == team]
        for i in range(len(board.POSSIBLE_MILL)):
            possibleFormMill = len(list(set(board.POSSIBLE_MILL[i]) & set(chess_on_board_list)))
            if possibleFormMill == 2:
                totalValue += VALUE_FOR_ONE_CHESS_REMAIN_TO_FORM_MILL
            elif possibleFormMill == 3:
                totalValue += VALUE_SUCCESSFULLY_FORM_MILL
        return totalValue

    def evaluate_block_mill_value(self, board, team):
        totalValue = 0
        VALUE_FOR_BLOCK_ENEMY_TO_FORM_MILL = 40

        chess_on_board_list = [i for i in range(16) if board.get_chess_in(i) == team]
        enemy_chess_on_board_list = [i for i in range(16) if board.get_chess_in(i) == (not team)]
        for i in range(len(board.POSSIBLE_MILL)):
            possibleFormMill = len(list(set(board.POSSIBLE_MILL[i]) & set(chess_on_board_list)))
            possibleEnemyFormMill = len(list(set(board.POSSIBLE_MILL[i]) & set(enemy_chess_on_board_list)))
            if possibleFormMill == 1 and possibleEnemyFormMill == 2:
                totalValue += VALUE_FOR_BLOCK_ENEMY_TO_FORM_MILL
        return totalValue

    def evaluation_board(self, team, board):
        totalValue = 0
        KILL_VALUE_MULTIPLIER = 3
        for i in range(16):
            if board.get_chess_in(i) == team:
                totalValue += self.BOARD_VALUE[i]
        if board.previous_state == board.BOARD_STATE_PLACE:
            # FIXME prevent opposite from forming mill
            totalValue += self.evaluate_block_mill_value(board, team)
        elif board.previous_state == board.BOARD_STATE_MOVE:
            # FIXME MOVE
            if board.current_state == board.BOARD_STATE_MOVE:
                return 0
            else:
                # Test current chess to move's freeness
                totalValue += self.evaluate_value_in(board, board.move_chess_temp)
                # Test possible mill
                totalValue += self.evaluate_mill_value(board, team)
                totalValue += self.evaluate_block_mill_value(board, team)
        elif board.previous_state == board.BOARD_STATE_MOVING:
            # Test all chess freeness
            for i in range(16):
                if board.get_chess_in(i) == team:
                    totalValue += self.evaluate_value_in(board, i)
            # Test possible mill
            totalValue += self.evaluate_mill_value(board, team)
            totalValue += self.evaluate_block_mill_value(board, team)

        elif board.previous_state == board.BOARD_STATE_KILLING:
            # FIXME KILL
            if board.current_state == board.BOARD_STATE_KILLING:
                return 0
            else:
                totalValue += self.BOARD_VALUE[board.latest_killed] * KILL_VALUE_MULTIPLIER

        return totalValue

    def search(self, board, max_depth, turn, team, depth=1, boundary=(-INF, INF)):
        best_act = -1
        if max_depth == depth or board.current_state == board.BOARD_STATE_ENDGAME:
            val = self.evaluation_board(team, board)
            return best_act, val

        possible_act_list = board.get_possible_act_list()
        # FIXME Take Turn
        for possible_act in possible_act_list:
            new_board = copy.deepcopy(self.game_board)
            new_board.act_chess(possible_act)
            temp, new_board_val = self.search(new_board, max_depth, not turn, team, depth+1, boundary)
            if new_board_val == self.INVALID:
                continue

            if turn == self.MYTURN:
                if boundary[0] < new_board_val:
                    boundary = (new_board_val, boundary[1])
                    best_act = possible_act
            else:
                if boundary[1] > new_board_val:
                    boundary = (boundary[0], new_board_val)
                    best_act = possible_act
            if boundary[0] > boundary[1]:
                return best_act, self.INVALID
            elif boundary[0] == boundary[1]:
                return best_act, boundary[0]

        if turn == self.MYTURN:
            return best_act, boundary[0]
        else:
            return best_act, boundary[1]