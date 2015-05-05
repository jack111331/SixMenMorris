import Othello_AI

#firstGameTreeStep(board,neighbor,startcolor,maxdepth,mm,chess,white,black)
#evaluation(board,x,y,chess,color,neighbor,white,black)

def create_probableMove(board):
	probable = []
	for y in range(8):
		for x in range(8):
			if board[y][x] == 0:
				probable.append((x,y))
	return probable

"""
board1 = [
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		]
"""

board1 = [
		[0,0,0,0,0,0,0,0],
		[0,2,2,2,0,0,0,0],
		[0,2,2,1,1,0,0,0],
		[0,0,2,1,1,0,0,0],
		[0,0,0,2,1,0,0,0],
		[0,0,0,2,1,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		]
board2 = [
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[2,0,0,0,0,0,0,0],
		[1,0,0,0,0,0,0,0],
		[2,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		]
board3 = [
		[0,1,0,1,2,2,0,0],
		[2,0,2,1,1,2,0,0],
		[2,0,2,1,1,0,0,0],
		[1,0,2,1,1,0,0,0],
		[2,2,2,2,1,0,0,0],
		[1,2,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		]
board4 = [
		[0,1,1,1,1,1,1,0],
		[1,0,2,1,1,2,0,0],
		[1,0,2,1,1,0,0,0],
		[1,0,2,2,1,0,0,0],
		[1,2,2,2,2,0,0,0],
		[1,2,1,0,0,0,0,0],
		[1,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		]
board5 = [
		[2,1,1,1,1,1,1,0],
		[1,2,2,1,1,2,0,1],
		[1,0,2,1,1,0,0,1],
		[1,0,2,1,1,0,0,1],
		[1,2,2,2,1,0,0,1],
		[1,2,1,0,0,0,0,1],
		[1,0,0,0,0,0,0,1],
		[0,1,1,1,1,1,1,0],
		]
board6 = [
		[0,1,0,0,0,0,0,0],
		[0,2,0,0,0,0,0,0],
		[0,2,1,0,0,0,0,0],
		[0,2,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		]
board7 = [
		[0,1,0,0,0,0,0,0],
		[0,2,0,0,0,0,0,0],
		[0,2,1,0,0,0,0,0],
		[0,2,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		]

print ("line: 1")
print (Othello_AI.evaluation(board1,0,0,14,1,create_probableMove(board1),6,8))
print ("line: 2")
print (Othello_AI.evaluation(board2,0,1,3,1,create_probableMove(board2),1,2))
print ("line: 3")
print (Othello_AI.evaluation(board3,2,0,25,1,create_probableMove(board3),12,13))
print ("line: 4")
print (Othello_AI.evaluation(board4,1,1,30,1,create_probableMove(board4),20,10))
print ("line: 5")
print (Othello_AI.evaluation(board5,2,0,42,1,create_probableMove(board5),32,10))
print ("line: 6")
print (Othello_AI.evaluation(board6,0,0,5,1,create_probableMove(board6),2,3))
print (Othello_AI.evaluation(board7,1,4,5,1,create_probableMove(board7),2,3))
print ("line: 7")
print ("line: 8")
print ("line: 9")
print ("line: 10")
print ("line: 11")
print ("line: 12")

