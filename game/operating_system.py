import asyncio
import pygame
import json

from custom_logging.logging import get_logger
from game.application import TerminalApplication
from game.applications.desktop_manager import DesktopManager
from game.applications.explorer import AuthenticFile
from game.applications.terminal import Terminal
from game.applications.vim import PilotTextEditor
from game.storage_system.directory import Directory
from game.storage_system.file import File
from exceptions.storage_system import SUPathError
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
			'AUTHENTICFILE': {
				'class': AuthenticFile,
				'instances': []
			},
			'DESKTOP': {
				'class': DesktopManager,
				'instances': []
			},
			'PILOTTEXTEDITOR': {
				'class': PilotTextEditor,
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
		self.start_application('TERMINAL', self, master_app=self.master_application)

		# prompt for username and password

		pass

	async def make_file(self, name, contents, parent):
		fl = File(name, contents, parent)
		parent.add(fl)
		return fl

	async def make_dir(self, name, contents, parent):
		dr = Directory(name, [], parent)
		for content in contents:
			if isinstance(content, Directory):
				await self.make_dir(content.get_name(), content.get_contents(), dr)
			else:
				await self.make_file(content.get_name(), content.get_contents(), dr)
		parent.add(dr)
		return dr

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				logger.info('Exiting Application...')
				pygame.quit()
				exit()

		self.master_application.event_queue += events

	def start_application(self, name, os, master_app=None, headless=False, *args, **kwargs):
		app = self.applications[name]['class'](self, os, *args, **kwargs)
		if not headless:
			app.surface = self.system.graphics.draw_application_window(*app.starting_size if master_app else self.system.graphics.conn_pygame_graphics.win.get_size(), (0, 255, 0), app.title if master_app else "", app.titlebar if master_app else False)
		if app.memory + self.memory_being_used > self.system.memory:
			raise Exception() # MAKE AND RAISE CUSTOM EXCEPTION WHICH WILL BE HANDLED OUTSIDE
		self.applications[name]['instances'].insert(0, app)
		if master_app:
			if master_app == self.master_application: 
				self.master_application.application_queue.insert(0, app)
				app.master_app = self.master_application
			elif master_app.master_app == self.master_application: 
				master_app.child_app = app #Only one app for non desktop managers
				app.master_app = master_app
				if isinstance(master_app, Terminal) and isinstance(app, TerminalApplication):
					app.surface = master_app.surface #copy by reference indeed
			else:
				raise Exception()  # Wrong OS instance / Machine
		else:
			self.master_application = app
		return app

	def su_open_in_app(self, su):
		for app in self.applications:
			for instance in self.applications[app]['instances']:
				if su == instance.current_dir or (isinstance(su, Directory) and su.has_su(instance.current_dir)):
					return True
		return False

	def parse_path(self, path, relative_to=None, parent_dir=False):
		original = path
		
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
				logger.error('relative_to variable not provided for a relative path. How did this even happen?')
				exit()
			current = relative_to

		if parent_dir: path = path[:-1]

		for part in path:
			if part == '..':
				if current == self.root:
					raise SUPathError(original, 'Cannot go further back than the root Directory.')
				current = current.get_parent()
			elif part == '.':
				continue
			else:
				try:
					current = current.get_su_by_name(part)
					if not current: raise SUPathError(original, 'Path not found.')
				except AttributeError:
					raise SUPathError(original, 'Path not found.')

		if checktype:
			if not isinstance(current, checktype):
				raise SUPathError(original, 'Path not found.')

		return current
