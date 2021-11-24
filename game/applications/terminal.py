import pygame
import random

from custom_logging.logging import get_logger
from game.application import Application
from game.constants import *
from utils.text import Text
from exceptions.applications import *


logger = get_logger('game')


class Terminal(Application):
	def __init__(self, os, opened_by):
		super().__init__(os, opened_by, 50)

		self.current_dir = os.root
		self.bg_colour = (25, 25, 60)
		self.starting_size = (720, 480)
		self.scale = 1
		self.title = 'TERMINAL'

		self.commands = {
			'pwd': self._pwd,
			'tree': self._tree,
			'clear': self._clear
		}

		chars = self.starting_size[0] // 10
		fontsize = (self.starting_size[0] / chars) * (5 / 3)

		self.content = Text(f'{self.get_new_line()}', (215, 215, 215), 'regular', fontsize, ending=[chars, ((self.starting_size[1] - titlebar_height) // fontsize)])
		self.stdin = ''

		self.wait_for_input = None

	def new_line(self):
		# logger.warn(self.content.get_raw_text())
		# logger.warn('------------------------------')
		self.update_content(f'\n\n{self.get_new_line()}')
		# logger.warn(self.content.get_raw_text())

	def get_new_line(self):
		return '${c:green}${s:bold}' + f'{self.os.username}' + '${c:reset}${s:reset}:${s:italic}' + f'{self.current_dir.get_path()}' + '${s:reset}$ '	

	def update_content(self, new):
		self.content.update_string(new)

	async def event_handler(self):
		await super().event_handler()
		if not self.current_event: return

		if self.current_event.type == pygame.KEYDOWN and self.current_event.key == pygame.K_RETURN:
			await self.run_command(self.stdin)
			self.stdin = ''

		if self.current_event.type == pygame.KEYDOWN and self.current_event.key == pygame.K_BACKSPACE:
			if len(self.stdin) > 0:
				self.stdin = self.stdin[:-1]
				self.content.string = self.content.string[:-1]
				self.content._process_string()
		

		if self.current_event.type == pygame.TEXTINPUT:
			self.stdin += self.current_event.text
			self.update_content(self.current_event.text)

		await self.event_handler()

	async def graphics_handler(self):
		await super().graphics_handler()
		self.os.system.graphics.display_terminal_text(self.surface, self.content)


	async def run_command(self, stdin):
		if self.wait_for_input: return self.wait_for_input(stdin)
		try:
			args = stdin.split(' ')
			cmd = args.pop(0)
			return await self.commands[cmd](args)
		except KeyError:
			return self.response(1, None, 'Command Not Recognised')

	def response(self, exit_code, stdout, stderr, update_in_terminal=True):
		if update_in_terminal:
			code = '${c:reset}' if not exit_code else '${c:red}' 
			self.update_content(code + f'\nExit code: {exit_code}' + '${c:reset}')
			if stdout: self.update_content(f'\n{stdout}')
			if stderr: self.update_content(code + f'\n{stderr}' + '${c:reset}')
			self.new_line()
		return { 'exit_code': exit_code, 'stdout': stdout, 'stderr': stderr }

	async def _pwd(self, _):
		return self.response(0, self.current_dir.get_path(), None)

	async def _tree(self, _):
		return self.response(0, self.current_dir.bfs(), None)

	async def _clear(self, _):
		self.content.update_string(self.get_new_line(), new=True)
		return self.response(0, None, None, update_in_terminal=False)

	async def _cd(self, args):
		path = '/' if len(args) < 1 else args[0]
