import pygame
import copy

from custom_logging.logging import get_logger
from exceptions.storage_system import SUNameError, SUPathError, DirectoryElementError
from game.application import Application
from game.constants import *
from game.storage_system.directory import Directory, RootDir
from game.storage_system.file import File
from utils.text import Text
from exceptions.applications import *


logger = get_logger('game')


class Terminal(Application):
	def __init__(self, os, opened_by):
		super().__init__(os, opened_by, 50)
		
		self.bg_colour = (48, 10, 36, 245)
		self.starting_size = (540, 360)
		self.scale = 1
		self.title = 'TERMINAL'

		self.commands = {
			'login': self._login,
			'ip': self._ip,
			'echo': self._echo,
			'pwd': self._pwd,
			'tree': self._tree,
			'ls': self._ls,
			'clear': self._clear,
			'cd': self._cd,
			'cat': self._cat,
			'rm': self._rm,
			'touch': self._touch,
			'mkdir': self._mkdir,
			'cp': self._cp,
			'mv': self._mv,
		}

		chars = self.starting_size[0] // 10
		fontsize = (self.starting_size[0] / chars) * (5 / 3)

		self.content = Text(f'{self.get_new_line()}', (200, 200, 200), 'regular', fontsize, startingpos= [3, 3], ending=[chars - 1, ((self.starting_size[1] - titlebar_height) // fontsize) - 1])
		self.stdin = ''

		self.wait_for_input = None
		self.hideinput = False

	def new_line(self):
		# logger.warn(self.content.get_raw_text())
		# logger.warn('------------------------------')
		self.update_content(f'\n{self.get_new_line()}')
		# logger.warn(self.content.get_raw_text())

	def get_new_line(self):
		return '${c:green}${s:italic}' + f'{self.os.username}' + '${c:reset}${s:reset}:' + '${c:blue}' + f'{self.current_dir.get_path()}' + '${c:reset}' + '> '	

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
				if not self.hideinput:
					self.content.string = self.content.string[:-1]
					self.content.process_string()

		if self.current_event.type == pygame.TEXTINPUT:
			self.stdin += self.current_event.text
			if not self.hideinput:
				self.update_content(self.current_event.text)

		await self.event_handler()

	async def graphics_handler(self):
		await super().graphics_handler()
		self.os.system.graphics.display_terminal_text(self.surface, self.content)

	async def run_command(self, stdin):
		if self.wait_for_input: return await self.wait_for_input(stdin)
		try:
			args = stdin.strip().split(' ')
			while '' in args: args.remove('')
			cmd = args.pop(0)
			return await self.commands[cmd.lower()](args)
		except KeyError:
			return self.response(1, None, 'Command Not Recognised')

	def response(self, exit_code, stdout, stderr, update_in_terminal=True):
		if update_in_terminal:
			code = '${c:reset}' if not exit_code else '${c:red}' 
			if exit_code: self.update_content(code + f'\nExit code: {exit_code}' + '${c:reset}')
			if stderr: self.update_content(code + f'\n{stderr}' + '${c:reset}')
			if stdout: self.update_content(f'\n{stdout}')
			self.new_line()
		return { 'exit_code': exit_code, 'stdout': stdout, 'stderr': stderr }

	async def _subcommand(self, content_update, subcommand_func):
		self.wait_for_input = subcommand_func
		self.update_content(content_update)

	async def _wait_for_password(self, password):
		self.wait_for_input = None
		self.hideinput = False
		if password == 'asyncxeno':
			return self.response(0, 'Logged in successfully.', None)
		else:
			return self.response(1, None, 'Incorrect Password.')

	async def _login(self, args):
		# username = args[0]
		await self._subcommand('\nPassword: ', self._wait_for_password)
		self.hideinput = True

	async def _ip(self, _):
		return self.response(0, self.os.system.get_ip(), None)

	async def _pwd(self, _):
		return self.response(0, self.current_dir.get_path(), None)

	async def _tree(self, _):
		return self.response(0, self.current_dir.bfs(), None)

	async def _ls(self, _):
		return self.response(0, '\n'.join([su.get_name() for su in self.current_dir.contents]), None)

	async def _clear(self, _):
		self.content.update_string(self.get_new_line(), new=True)
		return self.response(0, None, None, update_in_terminal=False)

	async def _echo(self, args):
		if '>>' in args:
			sep = args.index('>>')
			if not (len(args) - 1 > sep): return self.response(0, ' '.join(args), None)
			text = ' '.join(args[:sep])
			fl = args[sep + 1]
			try:
				su = self.os.parse_path(fl, self.current_dir)
			except SUPathError as e: return self.response(1, None, e.message)
			if not isinstance(su, File): return self.response(1, None, 'Argument after \'>>\' must be a file.')
			su.set_contents(text)
			return self.response(0, None, None)

		else:
			return self.response(0, ' '.join(args), None)

	async def _cd(self, args):
		path = '/' if len(args) < 1 else args[0]

		try:
			destination = self.os.parse_path(path, relative_to=self.current_dir)
		except SUPathError as e:
			return self.response(1, None, e.message)
		
		if not isinstance(destination, Directory): return self.response(1, None, 'No such directory found.')
		self.current_dir = destination
		return self.response(0, None, None)

	async def _cat(self, args):
		if len(args) < 1: return self.response(1, None, 'Too few Arguments. Use the \'help\' command for more info on commands.')

		try:
			su = self.os.parse_path(args[0], self.current_dir)
		except SUPathError as e:
			return self.response(1, None, e.message)

		if not isinstance(su, File): return self.response(1, None, 'Argument must be a File.')
		return self.response(0, str(su.get_contents()), None)
	
	async def _rm(self, args):
		if len(args) < 1: return self.response(1, None, 'Too few Arguments. Use the \'help\' command for more info on commands.')

		try:
			su = self.os.parse_path(args[0], self.current_dir)
			if self.os.su_open_in_app(su): return self.response(1, None, f'{su.__class__.__name__} is open in another application.')
		except SUPathError as e:
			return self.response(1, None, e.message)

		su.get_parent().delete(su.get_name())
		return self.response(0, None, None)

	async def _mkdir(self, args):
		if len(args) < 1: return self.response(1, None, 'Too few Arguments. Use the \'help\' command for more info on commands.')

		path = args[0].split('/')
		name = path.pop()
		if name == '': name = path.pop()

		if len(path) > 0:
			try:
				destination = self.os.parse_path(f'{"/".join(path)}/', self.current_dir)
			except SUPathError as e:
				return self.response(1, None, e.message)
		else: destination = self.current_dir

		try:
			await self.os.make_dir(name, [], destination)
		except SUPathError as e:
			return self.response(1, None, e.message)

		return self.response(0, None, None)

	async def _touch(self, args):
		if len(args) < 1: return self.response(1, None, 'Too few Arguments. Use the \'help\' command for more info on commands.')

		path = args[0].split('/')
		name = path.pop()
		if name == '': return self.response(1, None, 'You need to provide a file name.')

		if len(path) > 0:
			try:
				destination = self.os.parse_path(f'{"/".join(path)}/', self.current_dir)
			except SUPathError as e:
				return self.response(1, None, e.message)
		else: destination = self.current_dir 

		try:
			await self.os.make_file(name, '', destination)
		except SUPathError as e:
			return self.response(1, None, e.message)

		return self.response(0, None, None)

	async def _mv(self, args):
		if len(args) < 2:
			return self.response(1, None, 'Too few Arguments. Use the \'help\' command for more info on commands.')

		check_type = None

		old = args[0]
		new = args[1]
		new = new.split('/')
		if new[-1] == '':
			new.pop()
			check_type = Directory
		new = '/'.join(new)

		try:
			old = self.os.parse_path(old, relative_to=self.current_dir)
			if self.os.su_open_in_app(old): return self.response(1, None, f'{old.__class__.__name__} is open in another application.')
		except SUPathError as e:
			return self.response(1, None, e.message)
		
		try:
			new = self.os.parse_path(new, relative_to=self.current_dir)
		except SUPathError as e:
			try:
				new_dir = self.os.parse_path(new, relative_to=self.current_dir, parent_dir=True)
			except SUPathError as e:
				return self.response(1, None, e.message)
			if check_type:
				if not isinstance(old, Directory):
					return self.response(1, None, 'Cannot put a file as a directory.')
			if isinstance(old, Directory):
				if old.has_su(new_dir) or old == new_dir:
					return self.response(1, None ,'Cannot move a directory to a subdirectory of itself.')
			try:
				old.set_name(new.split('/')[-1])
			except SUNameError as e:
				return self.response(1, None, e.message)
			old.get_parent().delete(old.get_name())
			new_dir.add(old)
			return self.response(0, None, None)
		else:
			if not isinstance(new, Directory):
				return self.response(1, None, f'A {new.__class__.__name__} with that name already exists in the destination path.')
			else:
				if isinstance(old, Directory):
					if old.has_su(new) or old == new:
						return self.response(1, None ,'Cannot move a directory to a subdirectory of itself.')
				try:
					new.add(old)
				except DirectoryElementError as e:
					return self.response(1, None, e.message)
				return self.response(0, None, None)

	async def _cp(self, args):
		if len(args) < 2:
			return self.response(1, None, 'Too few arguments.\nSyntax: cp <oldpath> <newpath>')

		check_type = None

		old = args[0]
		new = args[1]
		new = new.split('/')
		if new[-1] == '':
			new.pop()
			check_type = Directory
		new = '/'.join(new)

		try:
			old = self.os.parse_path(old, relative_to=self.current_dir)
			if isinstance(old, RootDir):
				return self.response(1, None, 'Cannot copy root directory into itself.')
		except SUPathError as e:
			return self.response(1, None, e.message)
		
		try:
			new = self.os.parse_path(new, relative_to=self.current_dir)
		except SUPathError as e:
			try:
				new_dir = self.os.parse_path(new, relative_to=self.current_dir, parent_dir=True)
			except SUPathError as e:
				return self.response(1, None, e.message)
			if check_type:
				if not isinstance(old, Directory):
					return self.response(1, None, 'Cannot put a file as a directory.')
			try:
				if isinstance(old, File):
					await self.os.make_file(new.split('/')[-1], copy.deepcopy(old.get_contents()), new_dir)
				else:
					await self.os.make_dir(new.split('/')[-1], copy.deepcopy(old.get_contents()), new_dir)
			except DirectoryElementError as e:
				return self.response(1, None, e.message)
			return self.response(0, None, None)
		else:
			if not isinstance(new, Directory):
				return self.response(1, None, f'A {new.__class__.__name__} with that name already exists in the destination path.')
			else:
				try:
					if isinstance(old, File):
						await self.os.make_file(old.get_name(), copy.deepcopy(old.get_contents()), new)
					else:
						await self.os.make_dir(old.get_name(), copy.deepcopy(old.get_contents()), new)
				except DirectoryElementError as e:
					return self.response(1, None, e.message)
				return self.response(0, None, None)
