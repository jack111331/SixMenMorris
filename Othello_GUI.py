import pygame
import sys
import Othello_AI
from pygame.locals import *
from time import sleep

WHITE = (0, 0, 0)
BLACK = (221, 170, 0)
white_chess = pygame.image.load("image/white_chess.png")
black_chess = pygame.image.load("image/black_chess.png")
probable_moves = pygame.image.load("image/probable_moves.png")
multiple_play = pygame.image.load("image/multiple_play.png")
single_play = pygame.image.load("image/single_play.png")
number_list = {
	"0":pygame.image.load("image/number_0.png"),
	"1":pygame.image.load("image/number_1.png"),
	"2":pygame.image.load("image/number_2.png"),
	"3":pygame.image.load("image/number_3.png"),
	"4":pygame.image.load("image/number_4.png"),
	"5":pygame.image.load("image/number_5.png"),
	"6":pygame.image.load("image/number_6.png"),
	"7":pygame.image.load("image/number_7.png"),
	"8":pygame.image.load("image/number_8.png"),
	"9":pygame.image.load("image/number_9.png"),
}

AL_DIRECTION = [
	(-1, 1), (0, 1), (1, 1),
	(-1, 0), (1, 0),
	(-1, -1), (0, -1), (1, -1),
	]

class othelloBoardGame():
	def __init__(self):
		self.board = Board()
		self.players = []
	def define_players(self, firstplayer, secondplayer):
		self.players.append(firstplayer)
		self.players.append(secondplayer)

class othelloGui(othelloBoardGame):
	def check_event(self, game_status, window):
		for event in pygame.event.get():
			self.ifend(event)
			try:
				x, y = self.ifclick(event)
			except:
				pass
			else:
				if game_status == "begin":
					button1 = self.inrange(x, 100, 300, y, 0, 29)
					button2 = self.inrange(x, 100, 300, y, 40, 72)

					if button1:
						self.define_players(HumanPlayer(1), HumanPlayer(2))
						game_status = "multiple"
						self.board.draw_board(window)
					elif button2:
						self.define_players(ComputerPlayer(1), ComputerPlayer(2))
						game_status = "single_play"
						self.board.draw_board(window)

				elif (self.board.chess != 64 and str(self.players[self.board.turn-1]) == "human"): # single_play play
					x, y = x//50, y//50
					if (x, y) in self.board.probableMove:
						self.players[self.board.turn-1].flop(self.board, x, y, window)

		return game_status
	def inrange(self, x, str_x, end_x, y, str_y, end_y):
		if y > str_y and y < end_y:
			if x > str_x and x < end_x:
				return True
	def ifend(self, event):
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	def ifclick(self, event):
		if event.type == MOUSEBUTTONUP:
			return event.pos
		return False

class Board():
	def __init__(self):
		self.black = 2
		self.white = 2
		self.chess = 4
		self.board = [
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
		self.neighbor = [
			(2, 2), (3, 2), (4, 2), (5, 2),
			(2, 3), (5, 3),
			(2, 4), (5, 4),
			(2, 5), (3, 5), (4, 5), (5, 5),
			]
		self.turn = 1
		self.countLegalMoves()

	def checkempty(self, x, y, direction, color):# direction = (1, 0) right (-1, 0) left
		cross = []
		crossed = False
		while True:
			x += direction[0]
			y += direction[1]
			if x < 0 or x > 7 or y < 0 or y > 7 :
				break
			elif self.board[y][x] == 0:
				break
			elif self.board[y][x] != 0 and self.board[y][x] != color:
				cross.append((x, y))
			elif cross != [] and self.board[y][x] == color:
				crossed = True
				break
			elif cross == [] and self.board[y][x] == color:
				break
		if not crossed:
			return False
		return cross

	def legal_moves(self, color):
		moves = []
		for pos in self.neighbor:
			for dire in AL_DIRECTION:
				if self.checkempty(pos[0], pos[1], dire, color):
					moves.append(pos)
					break
		return moves

	def checkAllDir(self, x, y, color):
		cross = []
		for dire in AL_DIRECTION:
			a = self.checkempty(x, y, dire, color)
			if a:
				cross += a
		return cross

	def addNeighbor(self, x, y):
		self.neighbor.remove((x, y))

		for i in AL_DIRECTION:
			if x + i[0] > -1 and x + i[0] < 8 and y + i[1] > -1 and y + i[1] < 8:
				if self.board[y + i[1]][x + i[0]] == 0:
					if (x + i[0], y + i[1]) not in self.neighbor:
						self.neighbor.append((x + i[0], y + i[1]))

	def draw_board(self, window): 
		draw(window)
		window.fill(BLACK)
		draw(window)
		for i in range(8):
			for e in range(8):
				if self.board[e][i] != 0:
					if self.board[e][i] == 1:
						window.blit(white_chess,(i*50,e*50))
					else:
						window.blit(black_chess,(i*50,e*50))
		for i in self.probableMove:
			window.blit(probable_moves,(i[0]*50,i[1]*50))
		# white chess total
		window.blit(white_chess,(0,405))
		try:
			split_chess = str(self.white)[0],str(self.white)[1]
			window.blit(number_list[split_chess[0]], (50,403))
			window.blit(number_list[split_chess[1]], (100,403))
		except:
			split_chess = str(self.white)[0]
			window.blit(number_list[split_chess[0]], (50,404))
		# black chess total
		window.blit(black_chess,(350,405))
		try:
			split_chess = str(self.black)[0],str(self.black)[1]
			window.blit(number_list[split_chess[0]], (250,404))
			window.blit(number_list[split_chess[1]], (300,404))
		except:
			split_chess = str(self.black)[0]
			window.blit(number_list[split_chess[0]], (300,404))

	def changeplayer(self):
		if self.turn == 1:
			self.turn = 2
		else:
			self.turn = 1

	def countLegalMoves(self):
		self.probableMove = self.legal_moves(self.turn)

	def flop_board(self, x, y):
		self.board[y][x] = self.turn

		cross = self.checkAllDir(x, y, self.turn)

		if self.turn == 1:
			self.white += len(cross) + 1
			self.black -= len(cross)

		elif self.turn == 2:
			self.white -= len(cross)
			self.black += len(cross) + 1

		for i, j in cross:
			self.board[j][i] = self.turn
		self.addNeighbor(x, y)

	def winorlose(self):
		black = 0
		white = 0
		for i in self.board:
			for e in i:
				if e == 1:
					white += 1
				else:
					black += 1
		if white > black:
			return "white"
		return "black"

class Player():
	def __init__(self, color):
		self.color = color

	def flop(self, board, x, y, window):
		board.flop_board(x, y)
		board.chess += 1
		board.changeplayer()
		board.countLegalMoves()

		if board.probableMove == []:
			board.changeplayer()
			board.countLegalMoves()

		board.draw_board(window)
		pygame.display.flip()

		if board.chess == 64:
			win = board.winorlose()
			print (win + " is Winner")
			return "done"

class ComputerPlayer(Player):
	def next_move(self, board, window):

		len_legalMoves = board.legal_moves(self.color)
		if len_legalMoves:
			AI = Othello_AI.firstGameTreeStep(board,
				self.color,
				9)
			self.flop(board, AI[0], AI[1], window)
		else:
			board.changeplayer()
			board.countLegalMoves()
			board.draw_board(window)
			pygame.display.flip()

	def __str__(self):
		return "computer"

class HumanPlayer(Player):
	def __str__(self):
		return "human"

def draw(window):
	window.fill(BLACK)
	# row
	pygame.draw.line(window, WHITE, (46, 0), (46, 400), 5)# row 1
	pygame.draw.line(window, WHITE, (96, 0), (96, 400), 5)# row 2
	pygame.draw.line(window, WHITE, (146, 0), (146, 400), 5)# row 3
	pygame.draw.line(window, WHITE, (196, 0), (196, 400), 5)# row 4
	pygame.draw.line(window, WHITE, (246, 0), (246, 400), 5)# row 5
	pygame.draw.line(window, WHITE, (296, 0), (296, 400), 5)# row 6
	pygame.draw.line(window, WHITE, (346, 0), (346, 400), 5)# row 7
	# col
	pygame.draw.line(window, WHITE, (0, 46), (400, 46), 5)# col 1
	pygame.draw.line(window, WHITE, (0, 96), (400, 96), 5)# col 2
	pygame.draw.line(window, WHITE, (0, 146), (400, 146), 5)# col 3
	pygame.draw.line(window, WHITE, (0, 196), (400, 196), 5)# col 4
	pygame.draw.line(window, WHITE, (0, 246), (400, 246), 5)# col 5
	pygame.draw.line(window, WHITE, (0, 296), (400, 296), 5)# col 6
	pygame.draw.line(window, WHITE, (0, 346), (400, 346), 5)# col 7
	pygame.draw.line(window, WHITE, (0, 399), (400, 399), 4)# col 8

def othelloGuiGame():
	pygame.init()
	window = pygame.display.set_mode((400, 450))
	pygame.display.set_caption(' Othello ')
	window.fill(BLACK)
	window.blit(multiple_play, (100, 0))
	window.blit(single_play, (100, 40))
	game_status = "begin"
	OG = othelloGui()

	while True:
		game_status = OG.check_event(game_status, window)
		if len(OG.players) != 0:
			if OG.board.chess != 65 and str(OG.players[OG.board.turn-1]) == "computer":
				OG.players[OG.board.turn-1].next_move(OG.board, window)
				sleep(0.1)
		pygame.display.flip()

if __name__ == "__main__":
	othelloGuiGame()