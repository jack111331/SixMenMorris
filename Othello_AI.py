import Othello

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

def firstGameTreeStep(board, neighbor, startcolor, maxdepth, mm, chess, white, black):# now step is 1
	legalMoves = Othello.legal_moves(board, neighbor, startcolor)
	Best_chose = None
	next_mm = changeMAXMIN(mm)
	a = {}
	for i in legalMoves:
		next_board = []
		for e in board:
			next_board.append(e.copy())
		change = Othello.checkAllDir(board, i[0], i[1], startcolor)
		next_board[i[1]][i[0]] = startcolor
		next_board = Othello.flop(next_board, change, startcolor)
		next_neighbor = neighbor[::]
		next_neighbor = Othello.addNeighbor(next_board, next_neighbor, i[0], i[1])
		next_white = white
		next_black = black
		if startcolor == 1:
			next_white += len(change) + 1
			next_black -= len(change)
		elif startcolor == 2:
			next_white -= len(change)
			next_black += len(change) + 1
		next_color = changeplayer(startcolor)
		posible_way = nextGameTreeStep(next_board, next_neighbor, next_color, maxdepth, 2, a, next_mm, chess+1, next_white, next_black)
		if not Best_chose:
			Best_chose = (posible_way[0], i[0], i[1])
		elif type(posible_way[0]) == type(1):
			askkeep = choseMAXMIN(Best_chose[0], posible_way[0], mm)
			if askkeep:
				Best_chose = (posible_way[0], i[0], i[1])
	return Best_chose[0], (Best_chose[1], Best_chose[2])

def nextGameTreeStep(board, neighbor, color, maxdepth, depth, AlphaBeta, mm, chess, white, black):
	if depth >= maxdepth:
		Answer = evaluation(board, chess, color, neighbor, white, black)
		return (Answer, 0)
	else:
		legalMoves = Othello.legal_moves(board, neighbor, color)
		if not legalMoves:
			return evaluation(board, chess, color, neighbor, white, black)
		next_mm = changeMAXMIN(mm)
		new_depth = depth + 1
		for i in legalMoves:
			next_board = []
			for e in board:
				next_board.append(e.copy())
			change = Othello.checkAllDir(board, i[0], i[1], color)
			next_board[i[1]][i[0]] = color
			next_board = Othello.flop(next_board, change, color)
			next_neighbor = neighbor[::]
			next_white = white
			next_black = black
			if color == 1:
				next_white += len(change) + 1
				next_black -= len(change)
			elif color == 2:
				next_white -= len(change)
				next_black += len(change) + 1
			next_neighbor = Othello.addNeighbor(next_board, next_neighbor, i[0], i[1])
			next_color = changeplayer(color)
			posible_way = nextGameTreeStep(next_board, next_neighbor, next_color, 
				maxdepth, new_depth, AlphaBeta, next_mm, chess+1, next_white, next_black)
			# Alpha Beta Cut
			if posible_way:
				if depth - 2 in AlphaBeta:
					if mm == FINDMAX:
						if posible_way[0] < AlphaBeta[depth-2][0]:
							AlphaBeta[depth] = (posible_way[0], i)
							break
					elif mm == FINDMIN:
						if posible_way[0] > AlphaBeta[depth-2][0]:
							AlphaBeta[depth] = (posible_way[0], i)
							break
				elif depth not in AlphaBeta:
					AlphaBeta[depth] = (posible_way[0], i)
				else:
					askkeep = choseMAXMIN(AlphaBeta[depth][0], posible_way[0], mm)
					if askkeep:
						AlphaBeta[depth] = (posible_way[0], i)
		try:
			return AlphaBeta[depth]
		except:
			return False

def main(board, probableMove):
	return probableMove[0]

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
