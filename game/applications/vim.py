from logging import log
from utils.text import Text
from game.application import TerminalApplication
from game.applications.terminal import Terminal
from custom_logging.logging import get_logger
from game.constants import titlebar_height
from game.constants import titlebar_height
import pygame
import math

logger = get_logger('game')

def find_nth(string, substr, n):
	"""Finds nth occurance of a substring in a string 
	provided there are atleast n-1 number of 
	occurances of the substring within the string."""
	count=val=0
	for i in range(n):
		val = string.find(substr, val + int(val>0))
		count+=1
	if count == n-1:
		return len(string)-1
	return val

class PilotTextEditor(TerminalApplication):
	def __init__(self, os, opened_by, master_terminal, file):
		super().__init__(os, opened_by, 50)
		self.bg_colour=(30, 40, 34)
		self.modes = ['NORMAL', 'COMMAND', 'INSERT', 'VISUAL', 'VISUAL LINE', 'VISUAL BLOCK']
		self.cur_mode = 0
		self.keystrokes = ""
		self.cur_pos=[1,1]
		self.input_command=""
		self.scroll = 0
		self.changed = False
		self.editing_file = file
		self.font_size = master_terminal.fontsize*3/5
		self.key_cmds = {}
		self.skip = False
		self.stdin = file.get_contents()
		self.norm_controller = BaseNormVimCmd(self.key_cmds)
		self.run_commands = {}
		self.cursor = pygame.Surface((master_terminal.fontsize*3/5, master_terminal.fontsize))
		self.cursor.fill((255,255,255))
		self.cursor.set_alpha(0)
		self.cmd_controller = BaseRunVimCmd(self.run_commands)
		self.content = Text(self.add_line_num(self.stdin), (166, 226, 46), 'regular', master_terminal.fontsize, startingpos= [3, 3], ending=master_terminal.content.ending)
		self.status = Text(self.input_command, (166, 226, 46), 'regular', master_terminal.fontsize, startingpos= [3, master_terminal.starting_size[1]-titlebar_height-master_terminal.fontsize], ending=master_terminal.content.ending)

	async def run(self):
		await self.event_handler()
		await self.graphics_handler()

	def add_line_num(self, string):
		split_lines = string.split("\n")
		for i in range(len(split_lines)):
			split_lines[i] = " "*(4-len(str(i+1)))+ str(i+1)+"|" + split_lines[i]
		#logger.warn(len(split_lines))
		#logger.warn(self.cur_pos[1])
		split_lines[self.cur_pos[1]-1] = '⸸{c:white}' + split_lines[self.cur_pos[1]-1][:5] + '⸸{c:reset}'+split_lines[self.cur_pos[1]-1][5:]
		return "\n".join(split_lines)
	

	async def graphics_handler(self):
		await super().graphics_handler()
		T_half=500
		val = lambda x: 1 - pow(1 - x, 4)
		pass_val = lambda x: (T_half-abs(x%(2*T_half)-T_half))/T_half
		alpha = 155 * val(pass_val(pygame.time.get_ticks()))
		self.cursor.set_alpha(alpha) 
		cursor_rect = self.cursor.get_rect(topleft=(3+(self.cur_pos[0]+4)*self.font_size,titlebar_height+6+(self.cur_pos[1]-1)*self.font_size*5/3))
		self.surface.blit(self.cursor,cursor_rect)
		#self.cursor.topleft= (3+(self.cur_pos[0]-1)*self.font_size,titlebar_height+3+(self.cur_pos[1]-1)*self.font_size)
		self.os.system.graphics.display_terminal_text(self.surface, self.content)
		self.os.system.graphics.display_terminal_text(self.surface, self.status)

	async def event_handler(self):
		await super().event_handler()
		if not self.current_event: return

		#if self.current_event.type == pygame.KEYDOWN and self.current_event.key == pygame.K_RETURN:
			#await self.run_command(self.stdin)
			#self.stdin = ''

		if self.skip:
			self.skip = False
			await self.event_handler()
			return

		if self.current_event.type == pygame.TEXTINPUT:
			#When you type in insert mode.
			if self.cur_mode == self.modes.index("INSERT"):
				offset = sum([len(i)+1 for i in self.stdin.split("\n")[:self.cur_pos[1]-1]])+1 - (1 if len(self.stdin.split("\n"))==self.cur_pos[1] else 0)
				pos = offset + self.cur_pos[0]-1
				self.stdin = self.stdin[:pos] + self.current_event.text + self.stdin[pos:]
				if '\n' in self.current_event.text:
					self.cur_pos[1]+=1
				else:
					self.cur_pos[0]+=1
				if not self.hideinput:
					self.update_content(self.add_line_num(self.stdin), new=True)
				if self.content.string != self.editing_file.get_contents():
					self.changed = True 

		if self.current_event.type == pygame.KEYDOWN:
			if self.cur_mode == self.modes.index("INSERT"):
				#When you press Enter (to go to next line) in insert mode.
				if self.current_event.key == pygame.K_RETURN:
					offset = sum([len(i)+1 for i in self.stdin.split("\n")[:self.cur_pos[1]-1]])+1 - (1 if len(self.stdin.split("\n"))==self.cur_pos[1] else 0)
					pos = offset + self.cur_pos[0]-1
					self.stdin = self.stdin[:pos] + "\n" + self.stdin[pos:]
					self.cur_pos[:] = [1, self.cur_pos[1]+1]
					if not self.hideinput:
						self.update_content(self.add_line_num(self.stdin), new=True)
					if self.content.string != self.editing_file.get_contents():
						self.changed = True 
				#When you press backspace in insert mode
				elif self.current_event.key == pygame.K_BACKSPACE:
					if any([i > 1 for i in self.cur_pos]):
						offset = sum([len(i)+1 for i in self.stdin.split("\n")[:self.cur_pos[1]-1]])+1 - (1 if len(self.stdin.split("\n"))==self.cur_pos[1] else 0)
						pos = offset + self.cur_pos[0]-1 
						self.stdin = self.stdin[:pos-1] + self.stdin[pos:]
						self.cur_pos[1] = 1 if self.cur_pos[1]==1 else self.cur_pos[1]-1 if self.cur_pos[0] == 1 else self.cur_pos[1]
						if self.cur_pos[0] == 1:
							if self.cur_pos[1] > 1:
								self.cur_pos[0] = len(self.stdin.split("\n")[self.cur_pos[1]-1])+1
							else:
								self.cur_pos[0] = len(self.stdin.split("\n")[0])+1
						else:
							self.cur_pos[0]-=1
						logger.warn(self.cur_pos)
						if not self.hideinput:
							self.update_content(self.add_line_num(self.stdin), new=True)
						if self.content.string != self.editing_file.get_contents():
							self.changed = True 
			elif self.cur_mode == self.modes.index("COMMAND"):
				if self.current_event.key == pygame.K_BACKSPACE:
					self.input_command = self.input_command[:-1]
					self.status.update_string(self.input_command, new=True)
				elif self.current_event.key == pygame.K_RETURN:
					self.parse(self.input_command)
				elif self.current_event.key != pygame.K_ESCAPE:
					self.input_command += self.current_event.unicode
					self.status.update_string(self.input_command, new=True)
			if self.current_event.key == pygame.K_ESCAPE:
				self.clear_keystrokes()
				self.clear_command_entry()
				self.cur_mode = self.modes.index("NORMAL")
			if self.cur_mode == self.modes.index("NORMAL"):
				if not self.current_event.key == pygame.K_ESCAPE:
					self.skip = self.add_keystroke(self.current_event)

		await self.event_handler()
	
	def clear_keystrokes(self):
		self.keystrokes = ""

	def clear_command_entry(self):
		self.run_commands = ""

	def add_keystroke(self, key_event):
		if key_event.mod & pygame.KMOD_CTRL:
			self.keystrokes += "C-"
		self.keystrokes += key_event.unicode + " " 
		ret = self.execute_keystroke()
		if len(self.keystrokes.split()) > 4:
			self.clear_keystrokes()
		return ret
	
	def execute_keystroke(self):
		if "".join(self.keystrokes.split()) in self.key_cmds:
			self.key_cmds["".join(self.keystrokes.split())](self)
			self.clear_keystrokes()
			return True
		return False
	
	def parse(self, string):
		if string[0] == ":":
			if string[1:] in BaseRunVimCmd.cmd_dict:
				BaseRunVimCmd.cmd_dict[string[1:]](self)
			else:
				self.status.update_string("Not an editor command", True)
		elif string[0] == "/":
			pass
		self.cur_mode = self.modes.index("NORMAL")

class BaseNormVimCmd(object):

	def clr_keystroke(func):
		def inner(ref):
			func(ref)
			ref.clear_keystrokes()
		return inner

	def __init__(self, command_dict):
		BaseNormVimCmd.key_dict = {
			"i": BaseNormVimCmd.insert_mode, 
			":" : BaseNormVimCmd.command_mode,
			"h" : BaseNormVimCmd.move_left,
			"j" : BaseNormVimCmd.move_down,
			"k" : BaseNormVimCmd.move_up,
			"l" : BaseNormVimCmd.move_right,
			"d" : BaseNormVimCmd.debug,
		}
		command_dict.update(BaseNormVimCmd.key_dict)
		BaseNormVimCmd.key_dict = command_dict

	def __init_subclass__(cls):
		BaseNormVimCmd.key_dict.update(cls.key_dict)
	
	@staticmethod
	@clr_keystroke
	def insert_mode(ref):
		ref.cur_mode = ref.modes.index("INSERT")

	@staticmethod
	def command_mode(ref):
		ref.cur_mode = ref.modes.index("COMMAND")
		ref.input_command = ":"
	
	@staticmethod
	@clr_keystroke
	def move_left(ref):
		ref.cur_pos[0] = 1 if ref.cur_pos[0] == 1 else ref.cur_pos[0] - 1
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)
	
	@staticmethod
	@clr_keystroke
	def move_right(ref):
		lim = len(ref.stdin.split("\n")[ref.cur_pos[1]-1])
		ref.cur_pos[0] = lim+1 if ref.cur_pos[0] == lim+1 else ref.cur_pos[0] + 1
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)
	
	@staticmethod
	@clr_keystroke
	def move_down(ref):
		lim = ref.stdin.count("\n")
		ref.cur_pos[1] = lim+1 if ref.cur_pos[1] == lim+1 else ref.cur_pos[1] + 1
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)

	@staticmethod
	@clr_keystroke
	def move_up(ref):
		ref.cur_pos[1] = 1 if ref.cur_pos[1] == 1 else ref.cur_pos[1] - 1 
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)

	@staticmethod
	@clr_keystroke
	def debug(ref):
		logger.warn(ref.cur_pos)

class BaseRunVimCmd(object):

	def __init__(self, run_commands):
		BaseRunVimCmd.cmd_dict = {
			"w": BaseRunVimCmd.save,
			"q": BaseRunVimCmd.quit,
			"q!": BaseRunVimCmd.quit_over,
			"wq": BaseRunVimCmd.save_quit
		}
		run_commands.update(BaseRunVimCmd.cmd_dict)
		BaseRunVimCmd.cmd_dict = run_commands
	
	def __init_subclass__(cls):
		BaseRunVimCmd.cmd_dict.update(cls.cmd_dict)
	
	@staticmethod
	def save_quit(ref):
		ref.editing_file.set_contents(ref.stdin)
		ref.quit()
	
	@staticmethod
	def quit_over(ref):
		ref.quit()
	
	@staticmethod
	def quit(ref):
		if not ref.changed:
			ref.quit()
		else:
			ref.status.update_string("No write since last change (Add ! to override)", new=True)
		ref.clear_command_entry()

	@staticmethod
	def save(ref):
		ref.editing_file.set_contents(ref.stdin)
		ref.changed = False
		ref.clear_command_entry()
