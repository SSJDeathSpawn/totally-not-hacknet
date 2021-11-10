import pygame
import random

from custom_logging.logging import get_logger
from game.application import Application
from graphics.conn_pygame_graphics import Surface


logger = get_logger('game')


class Terminal(Application):
	def __init__(self, os, opened_by):
		super().__init__(os, opened_by, 50)

		self.current_dir = os.root
		self.bg_colour = (random.randint(0, 155), random.randint(0, 155), random.randint(0, 155))
		self.fg_colour = (255, 255, 255)
		self.starting_size = (540, 360)
		self.title = 'TERMINAL'

		self.commands = {
			'pwd': self.pwd
		}

		self.content = f'{self.new_line()}'
		self.stdin = ''

	def new_line(self):
		return f'{self.os.username}:{self.current_dir.get_path()}$ '

	def update_content(self, new):
		self.content += new
		if self.content.count('\n') > 300: self.content = '\n'.join(self.content.split('\n')[-300:])

	async def event_handler(self):
		await super().event_handler()
		if not self.current_event: return

		if self.current_event.type == pygame.KEYDOWN and self.current_event.key == pygame.K_RETURN:
			await self.run_command(self.stdin)
			self.stdin = ''
			self.update_content(f'\n{self.new_line()}')

		if self.current_event.type == pygame.KEYDOWN and self.current_event.key == pygame.K_BACKSPACE:
			if len(self.stdin) > 0:
				self.stdin = self.stdin[:-1]
				self.content = self.content[:-1]
		

		if self.current_event.type == pygame.TEXTINPUT:
			self.stdin += self.current_event.text
			self.update_content(self.current_event.text)

		await self.event_handler()

	async def graphics_handler(self):
		await super().graphics_handler()
		self.os.system.graphics.display_terminal_text(self.surface, self.content, self.fg_colour)


	async def run_command(self, stdin):
		try:
			args = stdin.split(' ')
			cmd = args.pop(0)
			await self.commands[cmd](args)
		except Exception: pass

	async def pwd(self, args):
		pass
