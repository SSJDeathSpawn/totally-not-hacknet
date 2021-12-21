from utils.text import Text
from game.application import TerminalApplication
from game.applications.terminal import Terminal
from custom_logging.logging import get_logger
import pygame

logger = get_logger('game')

class PilotTextEditor(TerminalApplication):
	def __init__(self, os, opened_by, master_terminal, file):
		super().__init__(os, opened_by, 50)
		self.bg_colour=(30, 40, 34)
		self.modes = ['NORMAL', 'COMMAND', 'INSERT', 'VISUAL', 'VISUAL LINE', 'VISUAL BLOCK']
		self.cur_mode = 0
		self.keystrokes = ""
		self.input_command=""
		self.changed = False
		self.editing_file = file
		self.key_cmds = {}
		self.norm_controller = BaseNormVimCmd(self.key_cmds)
		self.run_commands = {}
		self.comd_controller = BaseRunVimCmd(self.run_commands)
		self.content = Text("", (166, 226, 46), 'regular', master_terminal.fontsize, ending=master_terminal.content.ending)

	async def event_handler(self):
		await super().event_handler()
		if not self.current_event: return

		#if self.current_event.type == pygame.KEYDOWN and self.current_event.key == pygame.K_RETURN:
			#await self.run_command(self.stdin)
			#self.stdin = ''

		if self.current_event.type == pygame.TEXTINPUT:
			if self.cur_mode == self.modes.index("INSERT"):
				self.stdin += self.current_event.text
				if not self.hideinput:
					self.update_content(self.current_event.text)
				if self.content.string != self.editing_file.get_contents():
					self.changed = True 

		if self.current_event.type == pygame.KEYDOWN:
			if self.current_event.key == pygame.K_ESCAPE:
				self.clear_keystrokes()
				self.clear_command_entry()
				self.cur_mode = self.modes.index("NORMAL")
			if self.cur_mode == self.modes.index("NORMAL"):
				if not self.current_event.key == pygame.K_ESCAPE:
					self.add_keystroke(self.current_event)
			elif self.cur_mode == self.modes.index("INSERT") and self.current_event.key == pygame.K_BACKSPACE:
				if len(self.stdin) > 0:
					self.stdin = self.stdin[:-1]
					if not self.hideinput:
						self.content.string = self.content.string[:-1]
						self.content.process_string()

		await self.event_handler()
	
	def clear_keystrokes(self):
		self.keystrokes = ""

	def clear_command_entry(self):
		self.run_commands = ""

	def add_keystroke(self, key_event):
		logger.warn(self.keystrokes)
		if key_event.mod & pygame.KMOD_CTRL:
			self.keystrokes += "C-"
		self.keystrokes += key_event.unicode + " " 
		self.execute_keystroke()
		if len(self.keystrokes.split()) > 4:
			self.clear_keystrokes()
	
	def execute_keystroke(self):
		if "".join(self.keystrokes.split()) in self.key_cmds:
			self.key_cmds["".join(self.keystrokes.split())](self)

	async def graphics_handler(self):
		await super().graphics_handler()
		self.os.system.graphics.display_terminal_text(self.surface, self.content)

class BaseNormVimCmd(object):

	def __init__(self, command_dict):
		BaseNormVimCmd.key_dict = {"i": BaseNormVimCmd.insert_mode, ":" : BaseNormVimCmd.command_mode }
		command_dict.update(BaseNormVimCmd.key_dict)
		BaseNormVimCmd.key_dict = command_dict

	def __init_subclass__(cls):
		BaseNormVimCmd.key_dict.update(cls.key_dict)
	
	@staticmethod
	def insert_mode(ref):
		logger.warn("Somehow being called")
		ref.cur_mode = ref.modes.index("INSERT")

	@staticmethod
	def command_mode(ref):
		ref.cur_mode = ref.modes.index("COMMAND")
		ref.input_command = ":"
	
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