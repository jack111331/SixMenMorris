import pygame, sys
from pygame.locals import *
from time import sleep
import Othello, Othello_AI

def Othello():
	def __init__(self):
		pass
	def Gui(self):
		
		WHITE = (0,0,0)
		BLACK = (221,170,0)

def winorlose(board):
	if board.chess == 64:
		if board.white > board.black:
			return "white"
		return "black"
	elif board.white == 0:
		return "black"
	elif board.black == 0:
		return "white"
	else:
		return False

class Board():
	def __init__(self):
		self.black = 2
		self.white = 2
		self.chess = 4
		self.board = [
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
		self.neighbor = [
			(2,2),(3,2),(4,2),(5,2),
			(2,3),(5,3),
			(2,4),(5,4),
			(2,5),(3,5),(4,5),(5,5),
			]
		self.turn = 1
		self.countLegalMoves()
	def printout(self):
		Othello.pprint(self.board)
		print ("white:%i,black:%i,total:%i"%(self.white,self.black,self.chess))
		print ("turn:%i"%self.turn)
	def draw_board(self):
		global window
		win = winorlose(board)
		if win:
			print ("Player " + win + " is Winner")
			return "done"
		draw()
		window.fill(BLACK)
		draw()
		for i in range(8):
			for e in range(8):
				if self.board[e][i] != 0:
					if self.board[e][i] == 1:
						window.blit(white_chess,(i*50,e*50))
					else:
						window.blit(black_chess,(i*50,e*50))
		for i in self.probableMove:
			window.blit(probable_moves,(i[0]*50,i[1]*50))
	def changeplayer(self):
		if self.turn == 1:
			self.turn = 2
		else:
			self.turn = 1
	def countLegalMoves(self):
		self.probableMove = Othello.legal_moves(self.board,self.neighbor,self.turn)
	def flop_board(self,x,y):
		self.board[y][x] = self.turn
		cross = Othello.checkAllDir(self.board,x,y,self.turn)
		if self.turn == 1:
			self.white += len(cross) + 1
			self.black -= len(cross)
		elif self.turn == 2:
			self.white -= len(cross)
			self.black += len(cross) + 1
		self.board = Othello.flop(self.board,cross,self.turn)
		self.neighbor = Othello.addNeighbor(self.board,self.neighbor,x,y)

class Player():
	def __init__(self,color):
		self.color = color
	def flop(self,board,x,y):
		if board.chess == 64:
			win = Othello.winorlose(board.board)
			print (win + " is Winner")
			return "done"
		board.flop_board(x,y)
		board.chess += 1
		board.changeplayer()
		board.countLegalMoves()
		if board.probableMove == []:
			board.changeplayer()
			board.countLegalMoves()
		board.draw_board()
		pygame.display.flip()

class ComputerPlayer(Player):
	def next_move(self,board):
		FINDMAX = "max"
		copy_of_board = []
		for i in board.board:
			copy_of_board.append(i.copy())
		copy_of_neighbor = board.neighbor[::]
		if board.chess > 50 :
			AI = Othello_AI.firstGameTreeStep(copy_of_board,copy_of_neighbor,
				  self.color+1,10,FINDMAX,board.chess,board.white,board.black)
			self.flop(board,AI[1][0],AI[1][1])
		else:
			AI = Othello_AI.firstGameTreeStep(copy_of_board,copy_of_neighbor,
				  self.color+1,4,FINDMAX,board.chess,board.white,board.black)
			self.flop(board,AI[1][0],AI[1][1])
	def flop(self,board,x,y):
		super().flop(board,x,y)
	def __str__(self):
		return "computer"

class HumanPlayer(Player):
	def __str__(self):
		return "human"

def draw():
	global window
	window.fill(BLACK)
	# row
	pygame.draw.line(window, WHITE,(46,0),(46,400),5)# row 1
	pygame.draw.line(window, WHITE,(96,0),(96,400),5)# row 2
	pygame.draw.line(window, WHITE,(146,0),(146,400),5)# row 3
	pygame.draw.line(window, WHITE,(196,0),(196,400),5)# row 4
	pygame.draw.line(window, WHITE,(246,0),(246,400),5)# row 5
	pygame.draw.line(window, WHITE,(296,0),(296,400),5)# row 6
	pygame.draw.line(window, WHITE,(346,0),(346,400),5)# row 7
	# col
	pygame.draw.line(window, WHITE,(0,46),(400,46),5)# col 1
	pygame.draw.line(window, WHITE,(0,96),(400,96),5)# col 2
	pygame.draw.line(window, WHITE,(0,146),(400,146),5)# col 3
	pygame.draw.line(window, WHITE,(0,196),(400,196),5)# col 4
	pygame.draw.line(window, WHITE,(0,246),(400,246),5)# col 5
	pygame.draw.line(window, WHITE,(0,296),(400,296),5)# col 6
	pygame.draw.line(window, WHITE,(0,346),(400,346),5)# col 7
	pygame.draw.line(window, WHITE,(0,400),(400,400),5)# col 8

# def color
# load image
white_chess = pygame.image.load("image/white_chess.png")
black_chess = pygame.image.load("image/black_chess.png")
probable_moves = pygame.image.load("image/probable_moves.png")
multiple_play = pygame.image.load("image/multiple_play.png")
single_play = pygame.image.load("image/single_play.png")
#pygame
pygame.init()
window = pygame.display.set_mode((400, 450))
pygame.display.set_caption(' Othello ')

board = Board()
players = []
# draw select menu
window.fill(BLACK)
window.blit(multiple_play,(100, 0))
window.blit(single_play,(100, 40))
# does game begin
begin = False
while True: # main game loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONUP:
			if not begin:
				x, y = event.pos
				if y > 0 and y < 29:
					if x > 100 and x < 300:
						begin = "multiple"
						players = [HumanPlayer(0),HumanPlayer(1)]
						board.draw_board()
				elif y > 40 and y < 72:
					if x > 100 and x < 300:
						players = [HumanPlayer(0),ComputerPlayer(1)]
						begin = "single_play"
						board.draw_board()
			elif begin == "multiple" and board.chess != 64 and str(players[board.turn-1]) == "human": # single_play play
				x, y = event.pos
				x, y = x//50, y//50
				if (x, y) in board.probableMove:
					players[board.turn-1].flop(board,x,y)
			elif begin == "single_play" and board.chess != 64 and str(players[board.turn-1]) == "human": # AI
				x, y = event.pos
				x, y = x//50, y//50
				if (x, y) in board.probableMove:
					players[board.turn-1].flop(board,x,y)
	if begin == "single_play" and board.chess != 64 and str(players[board.turn-1]) == "computer":
		players[board.turn-1].next_move(board)
	pygame.display.flip()