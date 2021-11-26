import asyncio
import pygame
import json

from custom_logging.logging import get_logger
from game.applications.desktop_manager import DesktopManager
from game.applications.terminal import Terminal
from game.storage_system.directory import Directory, RootDir
from utils.storage_system_parser import parse_root


logger = get_logger('game')


class OperatingSystem(object):
	def __init__(self, system):
		self.system = system
		self.memory_being_used = 0
		with open('res/dev/root.json', 'r') as f:
			self.root = parse_root(json.load(f))
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
			},
			'DESKTOP': {
				'class': DesktopManager,
				'instances': []
			}
		}

		self.master_application = None

	async def run_main_loop(self):
		logger.info('Starting Main Loop...')
		while True:
			await asyncio.sleep(0)
			self.handle_events()
			await self.master_application.run()

	async def initialize(self):
		self.start_application('DESKTOP', self)

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

		self.master_application.event_queue += events

	def start_application(self, name, os, master_app=None, headless=False):
		app = self.applications[name]['class'](self, os)
		if not headless:
			app.surface = self.system.graphics.draw_application_window(*app.starting_size if master_app else self.system.graphics.conn_pygame_graphics.win.get_size(), (0, 255, 0), app.title if master_app else "", app.titlebar if master_app else False)
		if app.memory + self.memory_being_used > self.system.memory:
			raise Exception() # MAKE AND RAISE CUSTOM EXCEPTION WHICH WILL BE HANDLED OUTSIDE
		self.applications[name]['instances'].insert(0, app)
		if master_app:
			if master_app == self.master_application:
				self.master_application.application_queue.insert(0, app)
				app.master_app = self.master_application
			else:
				raise Exception()  # Wrong OS instance / Machine
		else:
			self.master_application = app
		return app

	def parse_path(self, path, relative_to=None, parent_dir=False):
		
		checktype = None
		path = path.strip()	

		if path in ['', '/']: return self.root
		path = path.split('/')
		if path[-1] == '':
			path.pop()
			checktype = Directory
		if path[0] == '':
			current = self.root
			path.pop(0)
		else:
			if not relative_to:
				raise Exception()  # I will make the exception later
			current = relative_to

		if parent_dir: path = path[:-1]

		for part in path:
			if part == '..':
				if current == self.root:
					raise Exception()  # I will make the exception later
				current = current.get_parent()
			elif part == '.':
				continue
			else:
				try:
					current = current.get_su_by_name(part)
				except Exception:
					raise Exception()  # I will make the exception later
				except AttributeError:
					raise Exception()  # Later

		if checktype:
			if not isinstance(current, checktype):
				raise Exception()  # later

		return current
