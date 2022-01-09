import pygame

from custom_logging.logging import get_logger
from game.constants import *


logger = get_logger('game')


class Application(object):
	def __init__(self, os, opened_by, memory):
		self.os = os
		self.current_dir = os.root
		self.opened_by = opened_by
		self.title = "Application"
		self.starting_size = (540, 360)
		self.memory = memory # In MBs
		self.is_being_moved = False
		self.bg_colour = (255,255,255)
		self.titlebar = True
		self.child_app = None

		self.event_queue = []
		self.current_event = None

		self.timer = 0
		self.timer_running = False

		logger.debug(f'Started a {self.__class__.__name__} Instance requested by OS with username {opened_by.username} ({opened_by.system.IP}).')

	async def event_handler(self):
		if len(self.event_queue) < 1:
			self.current_event = None
			return
		self.current_event = self.event_queue.pop(0)
		if not self.child_app:
			if self.os.modifiers["alt"] and self.current_event.type == pygame.KEYUP and self.current_event.key == pygame.K_F3:
				self.quit()

			if self.is_being_moved and self.current_event.type==pygame.MOUSEMOTION and self.current_event.buttons[0] == 1:
				min_val = (0, 0)
				max_val = (self.os.system.graphics.conn_pygame_graphics.win.get_width() - self.surface.get_width(), self.os.system.graphics.conn_pygame_graphics.win.get_height() - titlebar_height)
				self.surface.pos = max(min(self.surface.pos[0] + self.current_event.rel[0], max_val[0]), min_val[0]), max(min(self.surface.pos[1] + self.current_event.rel[1], max_val[1]), min_val[1])

			if self.current_event.type == pygame.MOUSEBUTTONDOWN and self.current_event.button==1:
				range_for_move = ((self.surface.pos[0], self.surface.pos[0] + self.surface.get_width()*(9/10)),
									(self.surface.pos[1], self.surface.pos[1]+self.surface.get_height()/10))
				range_for_close = ((self.surface.pos[0] + self.surface.get_width() * (9/10), self.surface.pos[0] + self.surface.get_width()),
									(self.surface.pos[1], self.surface.pos[1] + self.surface.get_height()/10))

				if (range_for_move[0][0] <= self.current_event.pos[0] <= range_for_move[0][1]) and (range_for_move[1][0] <= self.current_event.pos[1] <= range_for_move[1][1]):
					self.is_being_moved = True
				if (range_for_close[0][0] <= self.current_event.pos[0] <= range_for_close[0][1] ) and (range_for_close[1][0] <= self.current_event.pos[1] <= range_for_close[1][1]):
					self.quit()

			if self.is_being_moved and self.current_event.type == pygame.MOUSEBUTTONUP and self.current_event.button==1:
				self.is_being_moved = False
		else:
			self.child_app.event_queue += [self.current_event]

	async def graphics_handler(self):
		self.os.system.graphics.fill_application_window(self.surface, self.bg_colour)

	async def run(self):
		if self.timer_running:
			self.timer += self.os.system.graphics.conn_pygame_graphics.dt
			if self.timer >= double_click_window:
				self.timer_running = False
		await self.event_handler()
		if self.child_app:
			await self.child_app.run() 
		else:
			await self.graphics_handler()


	async def idle(self):
		pass

	async def input_event(self, event):
		self.event_queue.append(event)

	def quit(self):
		logger.debug(f'Quitting {self.__class__.__name__} Instance.')
		if isinstance(self.master_app, MasterApplication):
			self.os.system.graphics.conn_pygame_graphics.pop_surface(self.surface)
			self.master_app.application_queue.remove(self)
		else:
			self.master_app.child_app = None
		self.os.applications[self.__class__.__name__.upper()]['instances'].remove(self)

class MasterApplication(Application):
	def __init__(self, os, opened_by, memory):
		super().__init__(os, opened_by, memory)

		self.os = os
		self.opened_by = opened_by
		self.memory = memory
		self.application_queue = []
		self.event_queue = []
		self.current_event = None
		self.starting_size = self.os.system.graphics.conn_pygame_graphics.win.get_size()
		self.bg_colour = None
		self.titlebar = False

		logger.debug(f'Started a {self.__class__.__name__} Instance requested by OS with username {opened_by.username} ({opened_by.system.IP}).')
	
	async def event_handler(self):
		if len(self.event_queue) < 1:
			self.current_event = None
			return

	async def graphics_handler(self):
		pass

	async def idle(self):
		pass

	async def run(self):
		await self.event_handler()
		await self.graphics_handler()
		if self.application_queue:
			await self.application_queue[0].run()
			for app in self.application_queue[1:]:
				await app.idle()

class TerminalApplication(Application):
	def __init__(self, os, opened_by, memory):
		super().__init__(os, opened_by, memory)

		self.title = None
		self.starting_size = (540, 360)
		self.bg_colour = (255,255,255)
		self.titlebar = False
		self.child_app = None
		self.stdin = ''
		self.wait_for_input = None
		self.content = None
		self.hideinput = False
		logger.debug(f'Started a {self.__class__.__name__} Instance requested by OS with username {opened_by.username} ({opened_by.system.IP}).')

	async def event_handler(self):
		#logger.warn("Calling super")
		await super().event_handler()
	
	async def graphics_handler(self):
		await super().graphics_handler()

	def update_content(self, string, new=False):
		self.content.update_string(string, new=new)

	async def idle(self):
		pass

	async def run(self):
		if not self.child_app:
			await self.event_handler()
			await self.graphics_handler()
		else:
			await self.child_app.run()