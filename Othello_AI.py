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

def choseMAXMIN(Alpha,eva,mm):
	if mm == FINDMAX:
		if eva > Alpha:
			return eva
		return Alpha
	if eva < Alpha:
		return eva
	return Alpha

def evaluation(board,x,y,chess,color,neighbor,white,black):
	proportion = [
				(15,(7,2,1)),
				(30,(5,3,2)),
				(45,(3,4,3)),
				(60,(1,4,5)),
				(65,(0,0,10)),
				]
	GB = XYGoddOrBad(board,x,y)
	len_legal = nubmerLegalMove(board,neighbor,color)
	number = number_chess(color,white,black)
	for i in proportion:
		if chess <= i[0]:
			return ((GB * i[1][0]) + (len_legal * i[1][1]) + (number * i[1][2])) /10

def nubmerLegalMove(board,neighbor,color):
	return len(Othello.legal_moves(board,neighbor,color))

def XYGoddOrBad(board,x,y):
	board_GorB = [
				[4,-2,3,2,2,3,-2,4],
				[-2,-2,-1,-1,-1,-1,-2,-2],
				[3,-1,1,1,1,1,-1,3],
				[2,-1,1,0,0,1,-1,2],
				[2,-1,1,0,0,1,-1,2],
				[3,-1,1,1,1,1,-1,3],
				[-2,-2,-1,-1,-1,-1,-2,-2],
				[4,-2,3,2,2,3,-2,4],
				]
	return board_GorB[y][x]

def number_chess(color,white,black):
	if color == 1:
		return white - black
	return black - white

def firstGameTreeStep(board,neighbor,startcolor,maxdepth,mm,chess,white,black):# now step is 1
	legalMoves = Othello.legal_moves(board,neighbor,startcolor)
	Best_chose = None
	next_mm = changeMAXMIN(mm)
	for i in legalMoves:
		next_board = []
		for e in board:
			next_board.append(e.copy())
		change = Othello.checkAllDir(board,i[0],i[1],startcolor)
		next_board[i[1]][i[0]] = startcolor
		next_board = Othello.flop(next_board,change,startcolor)
		next_neighbor = neighbor[::]
		next_neighbor = Othello.addNeighbor(next_board,next_neighbor,i[0],i[1])
		next_white = white
		next_black = black
		if startcolor == 1:
			next_white += len(change) + 1
			next_black -= len(change)
		elif startcolor == 2:
			next_white -= len(change)
			next_black += len(change) + 1
		next_color = changeplayer(startcolor)
		posible_way = nextGameTreeStep(next_board,next_neighbor,next_color,maxdepth,2,{},next_mm,chess+1,next_white,next_black)
		if not Best_chose:
			Best_chose = (posible_way,(i[0],i[1]))
		elif type(Best_chose) == type(1):
			askkeep = choseMAXMIN(Best_chose,posible_way,mm)
			if askkeep:
				Best_chose = (posible_way,(i[0],i[1]))
	return Best_chose

def nextGameTreeStep(board,neighbor,color,maxdepth,depth,AlphaBeta,mm,chess,white,black):
	if depth >= maxdepth:
		legalMoves = Othello.legal_moves(board,neighbor,color)
		eva_list = []
		for i in legalMoves:
			a = evaluation(board,i[0],i[1],color,chess,neighbor,white,black)
			if depth - 2 in AlphaBeta:
				if mm == FINDMAX:
					if a < AlphaBeta[depth-2]:
						return a
				elif mm == FINDMIN:
					if a > AlphaBeta[depth-2]:
						return a
			eva_list.append(a)
		try:
			return max(eva_list)
		except:
			return 0
	else:
		legalMoves = Othello.legal_moves(board,neighbor,color)
		if not legalMoves:
			return False
		next_mm = changeMAXMIN(mm)
		new_depth = depth + 1
		for i in legalMoves:
			next_board = []
			for e in board:
				next_board.append(e.copy())
			change = Othello.checkAllDir(board,i[0],i[1],color)
			next_board[i[1]][i[0]] = color
			next_board = Othello.flop(next_board,change,color)
			next_neighbor = neighbor[::]
			next_white = white
			next_black = black
			if color == 1:
				next_white += len(change) + 1
				next_black -= len(change)
			elif color == 2:
				next_white -= len(change)
				next_black += len(change) + 1
			next_neighbor = Othello.addNeighbor(next_board,next_neighbor,i[0],i[1])
			next_color = changeplayer(color)
			posible_way = nextGameTreeStep(next_board,next_neighbor,next_color,
				maxdepth,new_depth,AlphaBeta,next_mm,chess+1,next_white,next_black)
			# Alpha Beta Cut
			if depth - 2 in AlphaBeta:
				if mm == FINDMAX:
					if posible_way < AlphaBeta[depth-2]:
						AlphaBeta[depth] = posible_way
						break
				elif mm == FINDMIN:
					if posible_way > AlphaBeta[depth-2]:
						AlphaBeta[depth] = posible_way
						break
			if posible_way:
				if depth not in AlphaBeta:
					AlphaBeta[depth] = posible_way
				else:
					askkeep = choseMAXMIN(AlphaBeta[depth],posible_way,mm)
					if askkeep:
						AlphaBeta[depth] = askkeep
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
		[0,0,0,0,0,0,0,0],# 0
		[0,0,0,0,0,0,0,0],# 1
		[0,0,0,0,0,0,0,0],# 2
		[0,0,0,1,2,0,0,0],# 3
		[0,0,0,2,1,0,0,0],# 4
		[0,0,0,0,0,0,0,0],# 5
		[0,0,0,0,0,0,0,0],# 6
		[0,0,0,0,0,0,0,0],# 7
		]
	neighbor = [
		(2,2),(3,2),(4,2),(5,2),
		(2,3),(5,3),
		(2,4),(5,4),
		(2,5),(3,5),(4,5),(5,5),
		]
	AI = fristGameTreeStep(board,neighbor,2,5,FINDMAX)
	print (AI)
