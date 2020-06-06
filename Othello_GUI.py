import pygame
import sys
import Othello_AI
import random
from pygame.locals import *
from pprint import pprint

WHITE = (0, 0, 0)
BLACK = (221, 170, 0)

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

CHESS_SIZE = 45

# Load Resource
white_chess = pygame.image.load("image/white_chess.png")
white_chess = pygame.transform.scale(white_chess, (CHESS_SIZE, CHESS_SIZE))
black_chess = pygame.image.load("image/black_chess.png")
black_chess = pygame.transform.scale(black_chess, (CHESS_SIZE, CHESS_SIZE))
board = pygame.image.load("image/board.png")
board = pygame.transform.scale(board, (WINDOW_WIDTH, WINDOW_HEIGHT))
probable_moves = pygame.image.load("image/probable_moves.png")
multiple_play = pygame.image.load("image/multiple_play.png")
single_play = pygame.image.load("image/single_play.png")

AL_DIRECTION = [
	(-1, 1), (0, 1), (1, 1),
	(-1, 0), (1, 0),
	(-1, -1), (0, -1), (1, -1)]


class othelloBoardGame():
	def __init__(self):
		self.board = Board()
		self.players = []

	def define_players(self, firstplayer, secondplayer):
		self.players.append(firstplayer)
		self.players.append(secondplayer)

class SixMenMorrisBoard():
	WHITE_CHESS = False
	BLACK_CHESS = True
	EMPTY = 6666666

	ACT_CHESS_SUCCESS = 1450666
	ACT_CHESS_OCCUPIED = 6661450
	ACT_CHESS_ILLEGAL = 6666

	BOARD_STATE_PLACE = 66666
	BOARD_STATE_MOVE = 66667
	BOARD_STATE_MOVING = 66668
	BOARD_STATE_KILLING = 66669
	BOARD_STATE_ENDGAME = 66670

	# Finite state machine
	#	--both player haven't placed all six chess<-												--- both player have > 2 chess   ---
	#	|									       |												|								   |
	#   v									       |												v								   |
	# Place chess |-> 	 not formed mill   ->      + -> both player have placed all six chess -> move chess |-> not formed mill   ->  -| -> one player has <= 2 chess -> End Game
	#             | 					           |														| 					       |
	#             | 					           |														|						   |
	# 			  ->    	form mill   ->    kill chess                                                    ->    form mill   ->  kill chess
	# 

	BESIDE_INDEX = [
		[1, 6],	[0, 2, 4], [1, 9],
		[4, 7],	[1, 3, 5], [4, 8],
		[0, 7, 13], [3, 6, 10], [5, 9, 12], [2, 8, 15],
		[7, 11], [10, 12, 14], [8, 11],
		[6, 14], [11, 13, 15], [9, 14]
	]

	POSSIBLE_MILL = [
		[0, 1, 2], 
		[3, 4, 5],
		[10, 11, 12],
		[13, 14, 15],
		[0, 6, 13], 
		[3, 7, 10], 
		[5, 8, 12], 
		[2, 9, 15] 
	]

	POSSIBLE_MILL_FOR_INDEX = [
		[0, 4], [0], [0, 7],
		[1, 5], [1], [1, 6],
		[4], [5], [6], [7],
		[2, 5], [2], [2, 6],
		[3, 4], [3], [3, 7]
	]

	def __init__(self):
		self.current_player = self.WHITE_CHESS
		self.current_state = self.BOARD_STATE_PLACE
		self.chess_list = [self.EMPTY] * 16
		self.placed_chess = 0
		self.move_chess_temp = -1

	def get_chess_in(self, index):
		return self.chess_list[index]

	def get_enemy(self):
		return not self.current_player

	def check_formed_mill(self, index):
		target_chess = self.get_chess_in(index)
		for i in range(len(self.POSSIBLE_MILL_FOR_INDEX[index])):
			check_three_chess = self.POSSIBLE_MILL_FOR_INDEX[index][i]
			found = True
			for j in range(len(self.POSSIBLE_MILL[check_three_chess])):
				check_chess_index = self.POSSIBLE_MILL[check_three_chess][j]
				if self.get_chess_in(check_chess_index) != target_chess:
					found = False
					break
			if found == True:
				return target_chess
		return self.EMPTY

	def place_chess(self, index):
		# FIXME if one can block another one's move?
		self.chess_list[index] = self.current_player
		self.placed_chess += 1

	def check_near(self, from_index, to_index):
		for i in range(len(self.BESIDE_INDEX[from_index])):
			if to_index == self.BESIDE_INDEX[from_index][i]:
				return True
		return False;

	def move_chess(self, from_index, to_index):
		# FIXME near
		if from_index == -1 or to_index == -1:
			print("Parameter error: ", from_index, to_index)
			return self.ACT_CHESS_ILLEGAL

		if self.get_chess_in(to_index) == self.get_enemy():
			return self.ACT_CHESS_ILLEGAL

		elif self.get_chess_in(to_index) == self.current_player:
			self.move_chess_temp = to_index
			return self.ACT_CHESS_OCCUPIED

		else:
			if self.check_near(from_index, to_index) == True:
				self.chess_list[to_index] = self.get_chess_in(from_index)
				self.chess_list[from_index] = self.EMPTY
				return self.ACT_CHESS_SUCCESS
			else:
				return self.ACT_CHESS_ILLEGAL

	def kill_chess(self, index):
		if self.check_formed_mill(index) == self.current_player:
			return self.ACT_CHESS_ILLEGAL
		self.chess_list[index] = self.EMPTY
		return self.ACT_CHESS_SUCCESS

	def change_player(self):
		self.current_player = not self.current_player

	def check_end_game(self):
		if self.placed_chess != 12:
			return False
		living_black_chess = 0
		living_white_chess = 0
		for i in range(len(self.BESIDE_INDEX)):
			if self.get_chess_in(i) == self.WHITE_CHESS:
				living_white_chess += 1
			elif self.get_chess_in(i) == self.BLACK_CHESS:
				living_black_chess += 1

		return living_black_chess <= 2 or living_white_chess <= 2

	def act_chess(self, index):
		if self.current_state == self.BOARD_STATE_PLACE:
			if self.get_chess_in(index) == self.EMPTY:
				self.place_chess(index)
				formed_mill = self.check_formed_mill(index)
				if formed_mill != self.EMPTY:
					self.current_state = self.BOARD_STATE_KILLING
				else:
					self.change_player()
				if self.placed_chess >= 12:
					self.current_state = self.BOARD_STATE_MOVE
				return self.ACT_CHESS_SUCCESS
			else:
				return self.ACT_CHESS_OCCUPIED

		elif self.current_state == self.BOARD_STATE_MOVE:
			if self.get_chess_in(index) != self.current_player:
				return self.ACT_CHESS_ILLEGAL
			self.move_chess_temp = index
			self.current_state = self.BOARD_STATE_MOVING
			return self.ACT_CHESS_SUCCESS

		elif self.current_state == self.BOARD_STATE_MOVING:
			act_result = self.move_chess(self.move_chess_temp, index)
			if act_result == self.ACT_CHESS_SUCCESS:
				self.move_chess_temp = -1
				if self.check_formed_mill(index) == self.current_player:
					self.current_state = self.BOARD_STATE_KILLING
				else:
					self.current_state = self.BOARD_STATE_MOVE
					self.change_player()
			return act_result

		elif self.current_state == self.BOARD_STATE_KILLING:
			if self.get_chess_in(index) != self.get_enemy():
				return self.ACT_CHESS_ILLEGAL
			else:
				act_result = self.kill_chess(index)
				if act_result == self.ACT_CHESS_SUCCESS:
					if self.check_end_game() == True:
						self.current_state = self.BOARD_STATE_ENDGAME
						return act_result
					elif self.placed_chess == 12:
						self.current_state = self.BOARD_STATE_MOVE
					else:
						self.current_state = self.BOARD_STATE_PLACE
					self.change_player()
				return act_result
		else:
			print("Unrecognize state")		

class SixMenMorrisScene():
	def __init__(self, window):
		self.window = window

	def change_scene(self):
		self.window.fill((BLACK))

	def check_event(self, event):
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	def ifclick(self, event):
		if event.type == MOUSEBUTTONUP:
			return event.pos
		return False

class SixMenMorrisMainMenuScene(SixMenMorrisScene):
	scene_name = "Main Menu"
	def __init__(self, window):
		super().__init__(window)

	def change_scene(self):
		super().change_scene()

	def check_event(self, event):
		super().check_event(event)

class SixMenMorrisInGameScene(SixMenMorrisScene):
	scene_name = "In Game"
	# detect coord range
	CHESS_COORD_RANGE = 30
	CHESS_COORD = [
		(100, 80), (510, 80), (920, 80),
		(305, 235), (510, 235), (715, 235),
		(100, 385), (305, 385), (715, 385), (920, 385),
		(305, 540), (510, 540), (715, 540),
		(100, 695), (510, 695), (920, 695)
	]

	# help map position to chess index

	CHESS_START_WIDTH = [
		0, 3, 6, 10, 13
	]

	BESIDE_INDEX = [
		[1, 6],	[0, 2, 4], [1, 9],
		[4, 7],	[1, 3, 5], [4, 8],
		[0, 7, 13], [3, 10], [5, 9, 12],
		[7, 11], [10, 12, 14], [8, 10],
		[6, 14], [10, 13, 15], [9, 14]
	]

	def __init__(self, window):
		super().__init__(window)
		self.game_state = None
		self.game_board = None

	def get_index(row, column):
		return SixMenMorrisInGameScene.CHESS_START_WIDTH[row] + column

	def assign_board(self, board):
		self.game_board = board

	def check_in_range(self, coord, index):
		target_coord = self.CHESS_COORD[index]
		return target_coord[0]+self.CHESS_COORD_RANGE >= coord[0] >= target_coord[0]-self.CHESS_COORD_RANGE \
			and target_coord[1]+self.CHESS_COORD_RANGE >= coord[1] >= target_coord[1]-self.CHESS_COORD_RANGE

	def update_scene(self):
		self.window.blit(board, (0, 0))
		if self.game_board != None:
			for i in range(len(self.CHESS_COORD)):
				chess_type_in_index = self.game_board.get_chess_in(i)
				correct_coord = (self.CHESS_COORD[i][0] - CHESS_SIZE/2, self.CHESS_COORD[i][1] - CHESS_SIZE/2)
				if chess_type_in_index == SixMenMorrisBoard.WHITE_CHESS:
					self.window.blit(white_chess, correct_coord)
				elif chess_type_in_index == SixMenMorrisBoard.BLACK_CHESS:
					self.window.blit(black_chess, correct_coord)
				else:
					pass
			pygame.display.flip()
		else:
			print("Board is none.")

	def change_scene(self):
		super().change_scene()
		self.update_scene();

	def check_event(self, event):
		super().check_event(event)
		try:
			x, y = self.ifclick(event)
			coord = (x, y)
		except Exception:
			pass
		else:
			click_index = None
			for i in range(len(self.CHESS_COORD)):
				if self.check_in_range(coord, i) == True:
					click_index = i
					break

			if click_index != None:
				place_chess_result = self.game_board.act_chess(click_index)
				if place_chess_result == SixMenMorrisBoard.ACT_CHESS_SUCCESS:
					print("Placed chess in ", click_index)
					self.update_scene()
				elif place_chess_result == SixMenMorrisBoard.ACT_CHESS_OCCUPIED:
					print("Place ", click_index, " occupied")
				elif place_chess_result == SixMenMorrisBoard.ACT_CHESS_ILLEGAL:
					print("Place ", click_index, " illegal")
				print("Current state: ", self.game_board.current_state)


class othelloGui(othelloBoardGame):
	def check_event(self, game_status, window):
		for event in pygame.event.get():
			self.ifend(event)
			try:
				x, y = self.ifclick(event)
			except Exception:
				pass
			else:
				print("clicked: ", x, y, "Status: ", game_status)
				if game_status == "begin":
					button1 = self.inrange(x, 100, 300, y, 0, 29)
					button2 = self.inrange(x, 100, 300, y, 40, 72)

					if button1:
						self.define_players(HumanPlayer(1), HumanPlayer(2))
						game_status = "multiple"
						self.board.draw_board(window)
					elif button2:
						self.define_players(HumanPlayer(1),
											ComputerPlayer(2, depth=3))
						game_status = "single_play"
						self.board.draw_board(window)

				elif (self.board.chess != 64 and
						str(self.players[self.board.turn - 1]) == "human"):
					# single_play play
					x, y = x // 50, y // 50
					if (x, y) in self.board.probableMove:
						self.players[self.board.turn - 1].flop(self.board,
															   x, y, window)

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
		self.end = False
		self.skip = 0

		self.black = 2
		self.white = 2
		self.chess = 4
		self.board = [
			# 0 1 2 3 4 5 6 7	   1 is white 2 is WHITE
			[0, 0, 0, 0, 0, 0, 0, 0],  # 0
			[0, 0, 0, 0, 0, 0, 0, 0],  # 1
			[0, 0, 0, 0, 0, 0, 0, 0],  # 2
			[0, 0, 0, 1, 2, 0, 0, 0],  # 3
			[0, 0, 0, 2, 1, 0, 0, 0],  # 4
			[0, 0, 0, 0, 0, 0, 0, 0],  # 5
			[0, 0, 0, 0, 0, 0, 0, 0],  # 6
			[0, 0, 0, 0, 0, 0, 0, 0]]  # 7

		self.neighbor = [
			(2, 2), (3, 2), (4, 2), (5, 2),
			(2, 3), (5, 3),
			(2, 4), (5, 4),
			(2, 5), (3, 5), (4, 5), (5, 5)]

		self.turn = 1
		self.countLegalMoves()

	def __repr__(self):
		pprint(self.board)
		return f"{self.black}, {self.white}, {self.chess}"

	def checkempty(self, x, y, direction, color):
		# direction = (1, 0) right (-1, 0) left

		cross = []
		crossed = False
		while True:
			x += direction[0]
			y += direction[1]
			if x < 0 or x > 7 or y < 0 or y > 7:
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
			if (x + i[0] > -1 and x + i[0] < 8 and
					y + i[1] > -1 and y + i[1] < 8):
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
						window.blit(white_chess, (i * 50, e * 50))
					else:
						window.blit(black_chess, (i * 50, e * 50))
		for i in self.probableMove:
			window.blit(probable_moves, (i[0] * 50, i[1] * 50))
		# white chess total
		window.blit(white_chess, (0, 405))
		try:
			split_chess = str(self.white)[0], str(self.white)[1]
			window.blit(number_list[split_chess[0]], (50, 403))
			window.blit(number_list[split_chess[1]], (100, 403))
		except Exception:
			split_chess = str(self.white)[0]
			window.blit(number_list[split_chess[0]], (50, 404))
		# black chess total
		window.blit(black_chess, (350, 405))
		try:
			split_chess = str(self.black)[0], str(self.black)[1]
			window.blit(number_list[split_chess[0]], (250, 404))
			window.blit(number_list[split_chess[1]], (300, 404))
		except Exception:
			split_chess = str(self.black)[0]
			window.blit(number_list[split_chess[0]], (300, 404))

	def changeplayer(self):
		if self.turn == 1:
			self.turn = 2
		else:
			self.turn = 1

	def countLegalMoves(self):
		self.probableMove = self.legal_moves(self.turn)

	def flip_chess(self, x, y):
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


class Player():
	def __init__(self, color):
		self.color = color

	def flop(self, board, x, y, window):
		board.flip_chess(x, y)
		board.chess += 1
		board.changeplayer()
		board.countLegalMoves()

		if board.probableMove == []:
			board.changeplayer()
			board.countLegalMoves()

		board.draw_board(window)
		pygame.display.flip()

		if board.chess == 64:
			self.end = True


class ComputerPlayer(Player):
	def __init__(self, color, depth=3):
		self.color = color
		self.depth = depth

	def next_move(self, board, window):
		try:
			moves = Othello_AI.find_max(board, self.depth)
			move = random.choice(moves)
			self.flop(board, move.pos[0], move.pos[1], window)
			board.skip = 0
		except Exception:
			board.changeplayer()
			board.countLegalMoves()
			board.draw_board(window)
			pygame.display.flip()

			board.skip += 1
			if board.skip == 2:
				board.end = True

	def __str__(self):
		return "computer"


class HumanPlayer(Player):
	def __str__(self):
		return "human"


def draw(window):
	window.fill(BLACK)
	# row
	pygame.draw.line(window, WHITE, (46, 0), (46, 400), 5)  # row 1
	pygame.draw.line(window, WHITE, (96, 0), (96, 400), 5)  # row 2
	pygame.draw.line(window, WHITE, (146, 0), (146, 400), 5)  # row 3
	pygame.draw.line(window, WHITE, (196, 0), (196, 400), 5)  # row 4
	pygame.draw.line(window, WHITE, (246, 0), (246, 400), 5)  # row 5
	pygame.draw.line(window, WHITE, (296, 0), (296, 400), 5)  # row 6
	pygame.draw.line(window, WHITE, (346, 0), (346, 400), 5)  # row 7
	# col
	pygame.draw.line(window, WHITE, (0, 46), (400, 46), 5)  # col 1
	pygame.draw.line(window, WHITE, (0, 96), (400, 96), 5)  # col 2
	pygame.draw.line(window, WHITE, (0, 146), (400, 146), 5)  # col 3
	pygame.draw.line(window, WHITE, (0, 196), (400, 196), 5)  # col 4
	pygame.draw.line(window, WHITE, (0, 246), (400, 246), 5)  # col 5
	pygame.draw.line(window, WHITE, (0, 296), (400, 296), 5)  # col 6
	pygame.draw.line(window, WHITE, (0, 346), (400, 346), 5)  # col 7
	pygame.draw.line(window, WHITE, (0, 399), (400, 399), 4)  # col 8


def SixMenMorrisGuiGame():
	pygame.init()
	pygame.font.init()
	window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption(" Six Men's Morris ")
	scene_pool = {
					SixMenMorrisMainMenuScene.scene_name: SixMenMorrisMainMenuScene(window), 
					SixMenMorrisInGameScene.scene_name: SixMenMorrisInGameScene(window) 
	}
	scene_pool[SixMenMorrisInGameScene.scene_name].assign_board(SixMenMorrisBoard())
	in_scene = SixMenMorrisInGameScene.scene_name
	scene_pool[in_scene].change_scene()

	# time = 10
	# white_win = []
	# black_win = []
	# draw = []

	# OG = othelloGui()
	# OG.define_players(HumanPlayer(1), ComputerPlayer(2, depth=1))
	# OG.board.draw_board(window)
	pygame.display.flip()


	while True:
		for event in pygame.event.get():
			scene_pool[in_scene].check_event(event)
	# while True:
		# game_status = OG.check_event(game_status, window)
		# for event in pygame.event.get():
		#	 if event.type == QUIT:
		#		 pygame.quit()
		#		 sys.exit()
		# if OG.board.end:
		#	 time -= 1
		#	 print(time)
		#	 if OG.board.white > OG.board.black:
		#		 white_win.append((OG.board.white, OG.board.black))
		#	 elif OG.board.white < OG.board.black:
		#		 black_win.append((OG.board.white, OG.board.black))
		#	 else:
		#		 draw.append((OG.board.white, OG.board.black))

		#	 if time == 0:
		#		 for record in white_win:
		#			 print("White is Winner")
		#			 print("%s : %s\n" % record)
		#		 for record in black_win:
		#			 print("Black is Winner")
		#			 print("%s : %s\n" % record)
		#		 for record in draw:
		#			 print("Draw")
		#			 print("%s : %s\n" % record)
		#		 pygame.quit()
		#		 sys.exit()

		#	 OG = othelloGui()
		#	 OG.define_players(ComputerPlayer(1, depth=3),
		#					   ComputerPlayer(2, depth=1))
		#	 OG.board.draw_board(window)
		# if len(OG.players) != 0:
		#	 if (OG.board.chess != 65 and
		#			 str(OG.players[OG.board.turn - 1]) == "computer"):
		#		 OG.players[OG.board.turn - 1].next_move(OG.board, window)
		#		 # break
		#		 # sleep(0.2)
		# pygame.display.flip()


if __name__ == "__main__":
	SixMenMorrisGuiGame()
