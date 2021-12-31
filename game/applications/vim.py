from logging import log
from utils.text import Text
from game.application import TerminalApplication
from game.applications.terminal import Terminal
from custom_logging.logging import get_logger
import pygame

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
		self.changed = False
		self.editing_file = file
		self.key_cmds = {}
		self.skip = False
		self.norm_controller = BaseNormVimCmd(self.key_cmds)
		self.run_commands = {}
		self.cmd_controller = BaseRunVimCmd(self.run_commands)
		self.content = Text("", (166, 226, 46), 'regular', master_terminal.fontsize, startingpos= [3, 3], ending=master_terminal.content.ending)

	def add_line_num(self, string):
		split_lines = string.split("\n")
		for i in range(len(split_lines)):
			split_lines[i] = " "*(4-len(str(i+1)))+ str(i+1)+"|" + split_lines[i]
		logger.warn(len(split_lines))
		logger.warn(self.cur_pos[1])
		split_lines[self.cur_pos[1]-1] = '⸸{c:white}' + split_lines[self.cur_pos[1]-1][:5] + '⸸{c:reset}'+split_lines[self.cur_pos[1]-1][5:]
		return "\n".join(split_lines)

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
				offset = find_nth(self.stdin, "\n", self.cur_pos[1]-1)+1
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
					offset = find_nth(self.stdin, "\n", self.cur_pos[1]-1)+1
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
						offset = find_nth(self.stdin, "\n", self.cur_pos[1]-1)+1
						pos = offset + self.cur_pos[0] - (1 if self.cur_pos[1]==1 else 0)
						self.stdin = self.stdin[:pos-2] + self.stdin[pos-1:]
						self.cur_pos[1] = 1 if self.cur_pos[1]==1 else self.cur_pos[1]-1 if self.cur_pos[0] == 1 else self.cur_pos[1]
						if self.cur_pos[0] == 1:
							if self.cur_pos[1] > 1:
								self.cur_pos[0] = (find_nth(self.stdin, "\n", self.cur_pos[1]) if len(self.stdin.split("\n")) > self.cur_pos[1] else len(self.stdin)-1) - find_nth(self.stdin, "\n", self.cur_pos[1]-1)+1
							else:
								self.cur_pos[0] = len(self.stdin.split("\n")[0])+1
						else:
							self.cur_pos[0]-=1
						if not self.hideinput:
							self.update_content(self.add_line_num(self.stdin), new=True)
						if self.content.string != self.editing_file.get_contents():
							self.changed = True 
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

	async def graphics_handler(self):
		await super().graphics_handler()
		self.os.system.graphics.display_terminal_text(self.surface, self.content)

class BaseNormVimCmd(object):

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
	def insert_mode(ref):
		ref.cur_mode = ref.modes.index("INSERT")
		ref.clear_keystrokes()

	@staticmethod
	def command_mode(ref):
		ref.cur_mode = ref.modes.index("COMMAND")
		ref.input_command = ":"
		ref.clear_keystrokes()
	
	@staticmethod
	def move_left(ref):
		ref.cur_pos[0] = 1 if ref.cur_pos[0] == 1 else ref.cur_pos[0] - 1
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)
		ref.clear_keystrokes()
	
	@staticmethod
	def move_right(ref):
		lim = len(ref.stdin.split("\n")[ref.cur_pos[1]-1])
		ref.cur_pos[0] = lim+1 if ref.cur_pos[0] == lim+1 else ref.cur_pos[0] + 1
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)
		ref.clear_keystrokes()
	
	@staticmethod
	def move_down(ref):
		lim = ref.stdin.count("\n")
		ref.cur_pos[1] = lim+1 if ref.cur_pos[1] == lim+1 else ref.cur_pos[1] + 1
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)
		ref.clear_keystrokes()

	@staticmethod
	def move_up(ref):
		ref.cur_pos[1] = 1 if ref.cur_pos[1] == 1 else ref.cur_pos[1] - 1 
		if not ref.hideinput:
			ref.update_content(ref.add_line_num(ref.stdin), new=True)
		ref.clear_keystrokes()

	@staticmethod
	def debug(ref):
		logger.warn(ref.cur_pos)

class BaseRunVimCmd(object):

	def __init__(self, run_commands):
		BaseRunVimCmd.cmd_dict = {}
		run_commands.update(BaseRunVimCmd.cmd_dict)
		BaseRunVimCmd.cmd_dict = run_commands
	
	def __init_subclass__(cls):
		BaseRunVimCmd.cmd_dict.update(cls.cmd_dict)

	@staticmethod
	def save(ref):
		ref.editing_file.set_contents(ref.content.string)
