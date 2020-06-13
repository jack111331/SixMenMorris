import pygame
import sys
from Six_Men_Morris_AI import *
import random
from pygame.locals import *
from pprint import pprint

WHITE = (0, 0, 0)
BLACK = (255, 255, 255)

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

CHESS_SIZE = 45
TIP_SIZE = 50

# Load Resource
BACKGROUND_IMG_RESOURCE = "image/background.png"
WHITE_CHESS_IMG_RESOURCE = "image/white_chess.png"
BLACK_CHESS_IMG_RESOURCE = "image/black_chess.png"
BOARD_IMG_RESOURCE = "image/board.png"
TIP_IMG_RESOURCE = "image/tip.png"
TIP_FOCUS_IMG_RESOURCE = "image/tip-focus.png"

game_font = None

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
		self.previous_state = self.BOARD_STATE_PLACE
		self.chess_list = [self.EMPTY] * 16
		self.placed_chess = 0
		self.move_chess_temp = -1
		self.latest_killed = -1
		self.chess_count = [0]*2
		self.kill_count = [0]*2

	def get_chess_in(self, index):
		return self.chess_list[index]

	def get_enemy(self):
		return not self.current_player

	def is_beside_has_empty(self, index):
		for i in range(len(self.BESIDE_INDEX[index])):
			if self.get_chess_in(self.BESIDE_INDEX[index][i]) == self.EMPTY:
				return True
		return False

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
		self.chess_count[self.current_player] += 1

	def check_near(self, from_index, to_index):
		for i in range(len(self.BESIDE_INDEX[from_index])):
			if to_index == self.BESIDE_INDEX[from_index][i]:
				return True
		return False;

	def move_chess(self, from_index, to_index):
		if from_index == -1 or to_index == -1:
			print("Parameter error: ", from_index, to_index)
			return self.ACT_CHESS_ILLEGAL

		if self.get_chess_in(to_index) == self.get_enemy():
			return self.ACT_CHESS_ILLEGAL

		elif self.get_chess_in(to_index) == self.current_player:
			self.move_chess_temp = to_index
			return self.ACT_CHESS_OCCUPIED

		else:
			if self.check_near(from_index, to_index) == True or self.chess_count[self.current_player] <= 3:
				self.chess_list[to_index] = self.get_chess_in(from_index)
				self.chess_list[from_index] = self.EMPTY
				return self.ACT_CHESS_SUCCESS
			else:
				return self.ACT_CHESS_ILLEGAL

	def kill_chess(self, index):
		if self.check_formed_mill(index) == self.current_player:
			return self.ACT_CHESS_ILLEGAL
		self.chess_count[self.chess_list[index]] -= 1
		self.kill_count[self.chess_list[index]] += 1
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

	def change_state(self, state):
		self.previous_state = self.current_state		
		self.current_state = state

	def act_chess(self, index):
		if self.current_state == self.BOARD_STATE_PLACE:
			if self.get_chess_in(index) == self.EMPTY:
				self.place_chess(index)
				formed_mill = self.check_formed_mill(index)
				if formed_mill != self.EMPTY:
					self.change_state(self.BOARD_STATE_KILLING)
				else:
					self.change_player()
				if self.placed_chess >= 12:
					self.change_state(self.BOARD_STATE_MOVE)
				return self.ACT_CHESS_SUCCESS
			else:
				return self.ACT_CHESS_OCCUPIED

		elif self.current_state == self.BOARD_STATE_MOVE:
			if self.get_chess_in(index) != self.current_player:
				return self.ACT_CHESS_ILLEGAL
			self.move_chess_temp = index
			self.change_state(self.BOARD_STATE_MOVING)
			return self.ACT_CHESS_SUCCESS

		elif self.current_state == self.BOARD_STATE_MOVING:
			act_result = self.move_chess(self.move_chess_temp, index)
			if act_result == self.ACT_CHESS_SUCCESS:
				self.move_chess_temp = -1
				if self.check_formed_mill(index) == self.current_player:
					self.change_state(self.BOARD_STATE_KILLING)
				else:
					self.change_state(self.BOARD_STATE_MOVE)
					self.change_player()
			return act_result

		elif self.current_state == self.BOARD_STATE_KILLING:
			if self.get_chess_in(index) != self.get_enemy():
				return self.ACT_CHESS_ILLEGAL
			else:
				act_result = self.kill_chess(index)
				if act_result == self.ACT_CHESS_SUCCESS:
					self.latest_killed = index
					if self.check_end_game() == True:
						self.change_state(self.BOARD_STATE_ENDGAME)
						return act_result
					elif self.placed_chess == 12:
						self.change_state(self.BOARD_STATE_MOVE)
					else:
						self.change_state(self.BOARD_STATE_PLACE)
					self.change_player()
				return act_result
		else:
			print("Unrecognize state")

	def get_possible_act_list(self):
		# TODO 
		if self.current_state == self.BOARD_STATE_PLACE:
			return [i for i in range(16) if self.get_chess_in(i) == self.EMPTY]
		elif self.current_state == self.BOARD_STATE_MOVE:
			if self.chess_count[self.current_player] <= 3:
				return [i for i in range(16) if self.get_chess_in(i) == self.current_player]				
			else:
				return [i for i in range(16) if (self.get_chess_in(i) == self.current_player and self.is_beside_has_empty(i) == True)]
		elif self.current_state == self.BOARD_STATE_MOVING:
			if self.chess_count[self.current_player] <= 3:
				return [i for i in range(16) if self.get_chess_in(i) == self.EMPTY]
			else:
				return [i for i in range(16) if (i in self.BESIDE_INDEX[self.move_chess_temp] and self.get_chess_in(i) == self.EMPTY)]
		elif self.current_state == self.BOARD_STATE_KILLING:
				return [i for i in range(16) if self.get_chess_in(i) == self.get_enemy()]

class Player():
	def __init__(self):
		self.team = None
		self.game_board = None

	def ifclick(self, event):
		if event.type == MOUSEBUTTONUP:
			return event.pos
		return False

	def assign_board(self, board):
		self.game_board = board

	def assign_team(self, team):
		self.team = team

	def act(self, event):
		pass


class ComputerPlayer(Player):
	def __init__(self, depth=8):
		super().__init__()
		self.depth = depth
		self.ai = None

	def assign_board(self, board):
		super().assign_board(board)
		self.ai = AlphaBetaPruning()

	def act(self, event):
		click_index, max_value = self.ai.search(self.game_board, self.depth, self.ai.MYTURN, self.game_board.current_player)
		print("AI choose index ", click_index, ", its value is ", max_value)
		place_chess_result = self.game_board.act_chess(click_index)

class HumanPlayer(Player):
	# detect coord range
	CHESS_COORD_RANGE = 30
	CHESS_COORD = [
		(100, 80), (510, 80), (920, 80),
		(305, 235), (510, 235), (715, 235),
		(100, 385), (305, 385), (715, 385), (920, 385),
		(305, 540), (510, 540), (715, 540),
		(100, 695), (510, 695), (920, 695)
	]

	def __init__(self):
		super().__init__()

	def check_in_range(self, coord, index):
		target_coord = self.CHESS_COORD[index]
		return target_coord[0]+self.CHESS_COORD_RANGE >= coord[0] >= target_coord[0]-self.CHESS_COORD_RANGE \
			and target_coord[1]+self.CHESS_COORD_RANGE >= coord[1] >= target_coord[1]-self.CHESS_COORD_RANGE

	def act(self, event):
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
				elif place_chess_result == SixMenMorrisBoard.ACT_CHESS_OCCUPIED:
					print("Place ", click_index, " occupied")
				elif place_chess_result == SixMenMorrisBoard.ACT_CHESS_ILLEGAL:
					print("Place ", click_index, " illegal")
				print("Current state: ", self.game_board.current_state)

class SixMenMorrisScene():
	in_scene = None
	scene_pool = {}
	def __init__(self, window):
		self.window = window

	def push_scene_into_pool(scene_name, scene):
		SixMenMorrisScene.scene_pool[scene_name] = scene

	def change_between_scene(scene_name):
		SixMenMorrisScene.in_scene = scene_name
		if SixMenMorrisScene.scene_pool[SixMenMorrisScene.in_scene] != None:
			SixMenMorrisScene.scene_pool[SixMenMorrisScene.in_scene].change_scene()
		else:
			print("No such scene")

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
		self.background = pygame.image.load(BACKGROUND_IMG_RESOURCE)
		self.background = pygame.transform.scale(self.background, (int(self.background.get_rect().size[0]*WINDOW_HEIGHT/WINDOW_WIDTH), WINDOW_HEIGHT))
		self.single_player_button = pygame.image.load("image/single_player_button.png")
		self.two_player_button = pygame.image.load("image/two_player_button.png")
		single_player_button_size = self.single_player_button.get_rect().size
		self.single_player_button_pos = (WINDOW_WIDTH/2 - single_player_button_size[0]/2, 500 - single_player_button_size[1]/2)
		two_player_button_pos_size = self.two_player_button.get_rect().size
		self.two_player_button_pos = (WINDOW_WIDTH/2 - two_player_button_pos_size[0]/2, 600 - two_player_button_pos_size[1]/2)
		self.background_pos = (int(WINDOW_WIDTH//2-self.background.get_rect().size[0]//2), 0)

	def change_scene(self):
		super().change_scene()
		self.window.blit(self.background, self.background_pos)
		self.window.blit(self.single_player_button, self.single_player_button_pos)
		self.window.blit(self.two_player_button, self.two_player_button_pos)
		pygame.display.flip()

	def check_event(self, event):
		super().check_event(event)
		try:
			x, y = self.ifclick(event)
			coord = (x, y)
		except Exception:
			pass
		else:
			if self.single_player_button_pos[0] <= coord[0] <= (self.single_player_button_pos[0] + self.single_player_button.get_rect().size[0]) and self.single_player_button_pos[1] <= coord[1] <= self.single_player_button_pos[1] + self.single_player_button.get_rect().size[1]:
				print("click single player button")
				SixMenMorrisScene.push_scene_into_pool(SixMenMorrisInGameScene.scene_name, SixMenMorrisInGameScene(self.window, [HumanPlayer(), ComputerPlayer()]))
				SixMenMorrisScene.scene_pool[SixMenMorrisInGameScene.scene_name].assign_board(SixMenMorrisBoard())
				SixMenMorrisScene.change_between_scene(SixMenMorrisInGameScene.scene_name)

			elif self.two_player_button_pos[0] <= coord[0] <= (self.two_player_button_pos[0] + self.two_player_button.get_rect().size[0]) and self.two_player_button_pos[1] <= coord[1] <= self.two_player_button_pos[1] + self.two_player_button.get_rect().size[1]:
				print("click two player button")
				SixMenMorrisScene.push_scene_into_pool(SixMenMorrisInGameScene.scene_name, SixMenMorrisInGameScene(self.window, [HumanPlayer(), HumanPlayer()]))
				SixMenMorrisScene.scene_pool[SixMenMorrisInGameScene.scene_name].assign_board(SixMenMorrisBoard())
				SixMenMorrisScene.change_between_scene(SixMenMorrisInGameScene.scene_name)

class SixMenMorrisEndGameScene(SixMenMorrisScene):
	scene_name = "End Game"
	END_GAME_TEXT_POSITION = (WINDOW_WIDTH/2, WINDOW_HEIGHT/3)
	def __init__(self, window):
		super().__init__(window)
		self.main_menu_button = pygame.image.load("image/main_menu_button.png")
		main_menu_button_size = self.main_menu_button.get_rect().size
		self.main_menu_button_pos = (WINDOW_WIDTH/2 - main_menu_button_size[0]/2, 500 - main_menu_button_size[1]/2)

	def change_scene(self):
		super().change_scene()
		self.window.blit(self.main_menu_button, self.main_menu_button_pos)
		game_font = pygame.font.SysFont("comicsansms", 72)
		if SixMenMorrisScene.scene_pool[SixMenMorrisInGameScene.scene_name].game_board.chess_count[0] <= 2:
			text = game_font.render("Black team wins", True, (0, 128, 196))
		else:
			text = game_font.render("White team wins", True, (0, 128, 196))
		self.window.blit(text, (int(self.END_GAME_TEXT_POSITION[0]-text.get_rect().size[0]//2), int(self.END_GAME_TEXT_POSITION[1]-text.get_rect().size[1]//2)))
		pygame.display.flip()

	def check_event(self, event):
		super().check_event(event)
		try:
			x, y = self.ifclick(event)
			coord = (x, y)
		except Exception:
			pass
		else:
			if self.main_menu_button_pos[0] <= coord[0] <= (self.main_menu_button_pos[0] + self.main_menu_button.get_rect().size[0]) and self.main_menu_button_pos[1] <= coord[1] <= self.main_menu_button_pos[1] + self.main_menu_button.get_rect().size[1]:
				print("click main menu button")
				SixMenMorrisScene.change_between_scene(SixMenMorrisMainMenuScene.scene_name)

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

	TURN_TEXT_POSITION = (WINDOW_WIDTH//2, WINDOW_HEIGHT//24)
	WHITE_EATEN_TEXT_POSITION = (WINDOW_WIDTH//6, WINDOW_HEIGHT//24*23)
	BLACK_EATEN_TEXT_POSITION = (WINDOW_WIDTH - WINDOW_WIDTH//6, WINDOW_HEIGHT//24*23)

	def __init__(self, window, players):
		super().__init__(window)
		self.game_board = None
		self.player_list = players
		self.white_chess_sprite = pygame.image.load(WHITE_CHESS_IMG_RESOURCE)
		self.white_chess_sprite = pygame.transform.scale(self.white_chess_sprite, (CHESS_SIZE, CHESS_SIZE))
		self.black_chess_sprite = pygame.image.load(BLACK_CHESS_IMG_RESOURCE)
		self.black_chess_sprite = pygame.transform.scale(self.black_chess_sprite, (CHESS_SIZE, CHESS_SIZE))
		self.board_sprite = pygame.image.load(BOARD_IMG_RESOURCE)
		self.board_sprite = pygame.transform.scale(self.board_sprite, (WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tip_sprite = pygame.image.load(TIP_IMG_RESOURCE)
		self.tip_sprite = pygame.transform.scale(self.tip_sprite, (TIP_SIZE, TIP_SIZE))
		self.tip_focus_sprite = pygame.image.load(TIP_FOCUS_IMG_RESOURCE)
		self.tip_focus_sprite = pygame.transform.scale(self.tip_focus_sprite, (TIP_SIZE, TIP_SIZE))

	def get_index(row, column):
		return SixMenMorrisInGameScene.CHESS_START_WIDTH[row] + column

	def assign_board(self, board):
		self.game_board = board
		for i in range(len(self.player_list)):
			self.player_list[i].assign_board(board)
			self.player_list[i].assign_team(bool(i))

	def update_scene(self):
		if self.game_board.current_state == self.game_board.BOARD_STATE_ENDGAME:
			SixMenMorrisScene.push_scene_into_pool(SixMenMorrisEndGameScene.scene_name, SixMenMorrisEndGameScene(self.window))
			SixMenMorrisScene.change_between_scene(SixMenMorrisEndGameScene.scene_name)
			return

		self.window.fill((BLACK))
		self.window.blit(self.board_sprite, (0, 0))
		# Display text
		game_font = pygame.font.SysFont("comicsansms", 60)
		if self.game_board.current_player == self.game_board.WHITE_CHESS:
			text = game_font.render("White team's turn", True, (0, 128, 196))
		else:
			text = game_font.render("Black team's turn", True, (0, 128, 196))			
		self.window.blit(text, (int(self.TURN_TEXT_POSITION[0]-text.get_rect().size[0]//2), int(self.TURN_TEXT_POSITION[1]-text.get_rect().size[1]//2)))

		game_font = pygame.font.SysFont("comicsansms", 30)
		text = game_font.render("White chess killed: " + str(self.game_board.kill_count[self.game_board.WHITE_CHESS]), True, (0, 128, 196))			
		self.window.blit(text, (int(self.WHITE_EATEN_TEXT_POSITION[0]-text.get_rect().size[0]//2), int(self.WHITE_EATEN_TEXT_POSITION[1]-text.get_rect().size[1]//2)))
		text = game_font.render("Black chess killed: " + str(self.game_board.kill_count[self.game_board.BLACK_CHESS]), True, (0, 128, 196))			
		self.window.blit(text, (int(self.BLACK_EATEN_TEXT_POSITION[0]-text.get_rect().size[0]//2), int(self.BLACK_EATEN_TEXT_POSITION[1]-text.get_rect().size[1]//2)))


		if self.game_board != None:
			possible_act_list = self.game_board.get_possible_act_list()
			for i in range(len(self.CHESS_COORD)):
				chess_type_in_index = self.game_board.get_chess_in(i)
				correct_chess_coord = (self.CHESS_COORD[i][0] - CHESS_SIZE/2, self.CHESS_COORD[i][1] - CHESS_SIZE/2)
				correct_tip_coord = (self.CHESS_COORD[i][0] - TIP_SIZE/2, self.CHESS_COORD[i][1] - TIP_SIZE/2)
				if chess_type_in_index == SixMenMorrisBoard.WHITE_CHESS:
					self.window.blit(self.white_chess_sprite, correct_chess_coord)
				elif chess_type_in_index == SixMenMorrisBoard.BLACK_CHESS:
					self.window.blit(self.black_chess_sprite, correct_chess_coord)
				if i in possible_act_list:
					self.window.blit(self.tip_sprite, correct_tip_coord)

			if self.game_board.move_chess_temp != -1:
				correct_tip_focus_coord = (self.CHESS_COORD[self.game_board.move_chess_temp][0] - TIP_SIZE/2, self.CHESS_COORD[self.game_board.move_chess_temp][1] - TIP_SIZE/2)
				self.window.blit(self.tip_focus_sprite, correct_tip_focus_coord)
			pygame.display.flip()
		else:
			print("Board is none.")

	def change_scene(self):
		super().change_scene()
		self.update_scene();

	def check_event(self, event):
		super().check_event(event)
		# FIXME when move, it work
		self.player_list[self.game_board.current_player].act(event)
		self.update_scene()


def SixMenMorrisGuiGame():
	pygame.init()
	pygame.font.init()

	window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption(" Six Men's Morris ")
	
	SixMenMorrisScene.push_scene_into_pool(SixMenMorrisMainMenuScene.scene_name, SixMenMorrisMainMenuScene(window))
	SixMenMorrisScene.change_between_scene(SixMenMorrisMainMenuScene.scene_name)

	while True:
		for event in pygame.event.get():
			SixMenMorrisScene.scene_pool[SixMenMorrisScene.in_scene].check_event(event)

if __name__ == "__main__":
	SixMenMorrisGuiGame()
