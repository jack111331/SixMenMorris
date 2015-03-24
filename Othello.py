from pprint import pprint

def checkempty(board,x,y,direction,color):# direction = (1,0) right (-1,0) left
	cross = []
	crossed = False
	while True:
		x += direction[0]
		y += direction[1]
		if x < 0 or x > 7 or y < 0 or y > 7 :
			break
		elif board[y][x] == 0:
			break
		elif board[y][x] != 0 and board[y][x] != color:
			cross.append((x,y))
		elif cross != [] and board[y][x] == color:
			crossed = True
			break
		elif cross == [] and board[y][x] == color:
			break
	if not crossed:
		return False
	return cross

def checkAllDir(board,x,y,color):
	allDirction = [
		(-1,1),(0,1),(1,1),
		(-1,0),(1,0),
		(-1,-1),(0,-1),(1,-1),
		]
	cross = []
	for dire in allDirction:
		a = checkempty(board,x,y,dire,color)
		if a:
			cross += a
	return cross

def legal_moves(board,neighbor,color):
	allDirction = [
		(-1,1),(0,1),(1,1),
		(-1,0),(1,0),
		(-1,-1),(0,-1),(1,-1),
		]
	moves = []
	for pos in neighbor:
		for dire in allDirction:
			a = checkempty(board,pos[0],pos[1],dire,color)
			if a:
				moves.append(pos)
				break
	return moves

def addNeighbor(board,neighbor,x,y):
	neighbor.remove((x,y))
	allDirction = [
		(-1,1),(0,1),(1,1),
		(-1,0),(1,0),
		(-1,-1),(0,-1),(1,-1),
		]
	for i in allDirction:
		if x+i[0] > -1 and x+i[0] < 8 and y+i[1] > -1 and y+i[1] < 8:
			if board[y+i[1]][x+i[0]] == 0:
				if (x+i[0],y+i[1]) not in neighbor:
					neighbor.append((x+i[0],y+i[1]))
	return neighbor

def flop(board,moves,color):
	for pos in moves:
		board[pos[1]][pos[0]] = color
	return board

def winorlose(board):
	black = 0
	white = 0
	for i in board:
		for e in i:
			if e == 1:
				white += 1
			else:
				black += 1
	if white > black:
		return "white"
	return "black"

def test():
	board = [
		#0 1 2 3 4 5 6 7       1 is white 2 is black
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
	turn  = 1
	chess = 4
	probableMove = legal_moves(board,neighbor,1)
	while True:
		print (probableMove)
		pos = raw_input()
		x,y = pos.split()
		x,y = int(x), int(y)
		if (x, y) in probableMove:
			board[y][x] = turn
			cross = checkAllDir(board,x,y,turn)
			board = flop(board,cross,turn)
			neighbor = addNeighbor(board,neighbor,x,y)
			chess += 1
			if turn == 1:
				turn = 2
			else:
				turn = 1
			probableMove = legal_moves(board,neighbor,turn)
			pprint(board)
			if chess == 64:
				win = winorlose(board)
				print (win + " is Winner")
				break
			print ("Change PLay to %i" % turn)
		else:
			print ("Error")


if __name__ == "__main__":
	test()