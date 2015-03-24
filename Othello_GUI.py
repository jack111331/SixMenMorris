import pygame, sys
from pygame.locals import *
from time import sleep
import Othello, Othello_AI

class Board():
	# const COLOR_W = 1;
	# const COLOR_B = 2;

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
		self.board = Othello.flop(self.board,cross,self.turn)
		self.neighbor = Othello.addNeighbor(self.board,self.neighbor,x,y)

class Player():
	def __init__(self,color):
		self.color = color
	def flop(self,board,x,y):
		board.flop_board(x,y)
		board.chess += 1
		board.changeplayer()
		if board.chess == 64:
			win = Othello.winorlose(board.board)
			print (win + " is Winner")
			return "done"
		board.countLegalMoves()
		if board.probableMove == []:
			board.changeplayer()
			board.countLegalMoves()
		board.draw_board()
		pygame.display.flip()

class ComputerPlayer(Player):
	def next_move():
		pass
	def flop(self,board,x,y):
		super().flop(board,x,y)
	def __str__(self):
		return "computer"

class HumenPlayer(Player):
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
WHITE = (122,122,122)
BLACK = (61,61,61)
# load image
white_chess = pygame.image.load("image/white_chess.png")
black_chess = pygame.image.load("image/black_chess.png")
probable_moves = pygame.image.load("image/probable_moves.png")
single_play = pygame.image.load("image/single_play.png")
multiple_play = pygame.image.load("image/multiple_play.png")
#pygame
pygame.init()
window = pygame.display.set_mode((400, 450))
pygame.display.set_caption(' Othello ')

board = Board()
players = []
# draw select menu
window.blit(single_play,(100, 0))
window.blit(multiple_play,(100, 40))
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
						players = [HumenPlayer(0),HumenPlayer(1)]
						board.draw_board()
				elif y > 40 and y < 72:
					if x > 100 and x < 300:
						players = [ComputerPlayer(0),ComputerPlayer(1)]
						begin = "single"
						board.draw_board()
			elif begin == "multiple" and board.chess != 64 and str(players[board.turn-1]) == "human": # single play
				x, y = event.pos
				x, y = x//50, y//50
				if (x, y) in board.probableMove:
					players[board.turn-1].flop(board,x,y)
			elif begin == "single" and board.chess != 64 and str(players[board.turn-1]) == "human": # AI
				x, y = event.pos
				x, y = x//50, y//50
				if (x, y) in board.probableMove:
					players[board.turn-1].flop(board,x,y)
	if begin == "single" and board.chess != 64 and str(players[board.turn-1]) == "computer":
		x, y = Othello_AI.main(board, board.probableMove)
		players[board.turn-1].flop(board,x,y)
		sleep(1)

	pygame.display.flip()