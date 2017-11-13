import Othello
from random import randint

PLAYER1 = 1
PLAYER2 = 2

FINDMAX = "max"
FINDMIN = "min"

def changeplayer(turn):
	if turn == PLAYER1:
		return PLAYER2
	return PLAYER1

def changeMAXMIN(mm):
	# if mm == FINDMAX:
	# 	return FINDMIN
	return FINDMAX

def choseMAXMIN(Alpha, eva, mm):
	if mm == FINDMAX:
		if eva > Alpha:
			return True
		return False
	if eva < Alpha:
		return True
	return False

def evaluation(board, chess, color, neighbor, white, black):
	proportion = [
				(10, (8, 1, 2)), 
				(20, (7, 2, 2)), 
				(30, (6, 3, 2)), 
				(40, (5, 4, 2)), 
				(100, (3, 4, 3)), 
				(55, (3, 3, 4)), 
				(65, (0, 0, 10)), 
				]
	GB = XYGoddOrBad(board, color)
	len_legal = nubmerLegalMove(board, neighbor, color)
	number = number_chess(color, white, black)
	for i in proportion:
		if chess <= i[0]:
			Answer = ((GB * i[1][0]) + (len_legal * i[1][1]) + (number * i[1][2]))
			return Answer

def nubmerLegalMove(board, neighbor, color):
	return len(Othello.legal_moves(board, neighbor, color))

def XYGoddOrBad(board, color):
	board_GorB = [
				[100, -10, 6, 3, 3, 6, -10, 100], 
				[-10, -10, -5, -5, -5, -5, -10, -10], 
				[6, -5, 4, 4, 4, 4, -5, 6], 
				[3, -5, 4, 1, 1, 4, -5, 3], 
				[3, -5, 4, 1, 1, 4, -5, 3], 
				[6, -5, 4, 4, 4, 4, -5, 6], 
				[-10, -10, -5, -5, -5, -5, -10, -10], 
				[100, -10, 6, 3, 3, 6, -10, 100], 
				]
	total = 0
	for y in range(8):
		for x in range(8):
			if color == 1:
				if board[y][x] == 1:
					total += board_GorB[y][x]
				elif board[y][x] == 2:
					total -= board_GorB[y][x]
			elif color == 2:
				if board[y][x] == 1:
					total -= board_GorB[y][x]
				elif board[y][x] == 2:
					total += board_GorB[y][x]
	return total

def number_chess(color, white, black):
	if color == 1:
		return white - black
	return black - white

def firstGameTreeStep(board, startcolor, maxdepth):
	return board.probableMove[0]

if __name__ == "__main__":
	# main()
	board = [
		#0 1 2 3 4 5 6 7       1 is white 2 is WHITE
		[0, 0, 0, 0, 0, 0, 0, 0], # 0
		[0, 0, 0, 0, 0, 0, 0, 0], # 1
		[0, 0, 0, 0, 0, 0, 0, 0], # 2
		[0, 0, 0, 1, 2, 0, 0, 0], # 3
		[0, 0, 0, 2, 1, 0, 0, 0], # 4
		[0, 0, 0, 0, 0, 0, 0, 0], # 5
		[0, 0, 0, 0, 0, 0, 0, 0], # 6
		[0, 0, 0, 0, 0, 0, 0, 0], # 7
		]
	neighbor = [
		(2, 2), (3, 2), (4, 2), (5, 2), 
		(2, 3), (5, 3), 
		(2, 4), (5, 4), 
		(2, 5), (3, 5), (4, 5), (5, 5), 
		]
	AI = fristGameTreeStep(board, neighbor, 2, 5, FINDMAX)
	print (AI)
