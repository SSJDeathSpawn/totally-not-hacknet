import asyncio
import pygame

from custom_logging.logging import get_logger
from game.applications.terminal import Terminal


logger = get_logger('game')


class OperatingSystem(object):
	def __init__(self, system):
		self.system = system
		self.memory_being_used = 0
		self.modifiers = {
			"shift": False,
			"alt": False,
			"ctrl": False
		}

		# Just for now
		self.username = 'asyncxeno'
		self.password = None

		self.applications = {
			'TERMINAL': {
				'class': Terminal,
				'instances': []
			}
		}

		self.application_queue = []

	async def run_main_loop(self):
		logger.info('Starting Main Loop...')
		while True:
			await asyncio.sleep(0)
			if len(self.application_queue) > 0:
				await self.application_queue[0].run()
				if len(self.application_queue) > 1:
					for application in self.application_queue[1:]:
						await application.idle()

	async def initialize(self):
		self.start_application('TERMINAL', self)

		# prompt for username and password

		pass

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				logger.info('Exiting Application...')
				pygame.quit()
				exit()

			if event.type in (pygame.KEYDOWN, pygame.KEYUP):
				if event.key in (pygame.K_LALT, pygame.K_RALT):
					self.modifiers["alt"] = False if event.type == pygame.KEYUP else True
				elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
					self.modifiers["shift"] = False if event.type == pygame.KEYUP else True
				elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
					self.modifiers["alt"] = False if event.type == pygame.KEYUP else True

			if self.modifiers["alt"] and event.type == pygame.KEYUP and event.key == pygame.K_F3:
				self.application_queue[0].quit()

		for application in self.application_queue:
			application.event_queue += events

	def start_application(self, name, os):
		app = self.applications[name]['class'](self, os)
		if app.memory + self.memory_being_used > self.system.memory:
			raise Exception() # MAKE AND RAISE CUSTOM EXCEPTION WHICH WILL BE HANDLED OUTSIDE
		self.applications[name]['instances'].append(app)
		self.application_queue.append(app)
		return app
