from __future__ import annotations

import pygame.event
import pygame.time

from typing import TYPE_CHECKING, Type
from concurrent.futures import ThreadPoolExecutor
from logging import Logger
from game.applications.terminal import Terminal
from game.command import Response, Command
from logging_module.custom_logging import get_logger
from utils.general_utils import generate_pid
from utils.math import between
from utils.deserializer import deserialize_root_directory
from game.storage_system.directory import RootDir, Directory
from game.storage_system.file import File
from exceptions.storage_system import PathError
from game.applications.desktop import Desktop
from game.applications.explorer import Explorer
from game.constants import APPLICATIONS, DEFAULT_ROOTDIR_PATH
from game.applications.application import Application, ApplicationInstance
from commands.basic import ls, cd, exit, cat

if TYPE_CHECKING:
    from game.system import System
    from graphics.conn_pygame_graphics import Surface


class OperatingSystem(object):
    """Class representing an Operating System"""
    
    def __init__(self, system: System, root: RootDir) -> None:
        
        self.logger: Logger = get_logger('game')
        self.system: System = system
        self.root: RootDir = deserialize_root_directory(DEFAULT_ROOTDIR_PATH)

        # # TODO: very short term temporary code pls remove asap
        # self.root.add(Directory(self.root, 'dir1', []))
        # self.root.add(Directory(self.root, 'dir2', []))
        # self.root.add(File(self.root, 'file1', 'abc'))
        # self.root.get_su_by_name('dir1').add(File(self.root.get_su_by_name('dir1'), 'hello.txt', 'Do not speak of this'))

        self.events: list[pygame.event.Event] = []

        self.installed_apps: dict[str, Type[Application]] = APPLICATIONS

        self.running = True
        self.running_apps: set[ApplicationInstance] = set()

        self.startup_apps: dict[Application, bool] = {
            # class: is_bg
            Desktop: False,
            Terminal: False
        }

        self.commands = {
            'ls': Command('ls', ls, ''),
            'cd': Command('cd', cd, ''),
            'exit': Command('exit', exit, ''),
            'cat': Command('cat', cat, '')
            # TODO: Put man entires as constants later on
        }

        self.command_backlog: list[str] = []

        self.selected: ApplicationInstance

        self.executor: ThreadPoolExecutor = ThreadPoolExecutor()
        self.temp = None

    # Helpers

    def get_su_by_path(self, path: str, current_dir: Directory) -> Directory:
        """Returns a storage unit by path"""

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
            current = current_dir

        for part in path:
            if part == '..':
                if current == self.root:
                    return self.root
                current = current.get_parent()

            elif part == '.':
                continue

            else:
                try:
                    current = current.get_su_by_name(part)
                    if not current: 
                        raise PathError(f'no such file or directory: {original}')
                except AttributeError:
                    raise PathError(f'no such file or directory: {original}')

        if checktype and not isinstance(current, checktype):
            raise PathError(f'no such file or directory: {original}')

        return current

    # Main

    def execute_command(self, app: Application, name: str, args: list[str]) -> Response:
        """Executes a command for an application"""

        if name not in self.commands.keys():
            return Response(127, '', f'{name}: command not found')

        self.logger.debug('command')
        return self.commands.get(name)(app, *args)

    def boot(self) -> None:
        """Boots up the Operating System"""
        
        for app in self.startup_apps:
            self.start_app(app, self, self.startup_apps.get(app))

    def start_app(self, app: Type[Application], opened_by: OperatingSystem, open_in_bg: bool = False) -> ApplicationInstance:
        """Starts a new application instance"""

        instance = ApplicationInstance(app(self, opened_by=opened_by), generate_pid(), open_in_bg)

        self.running_apps.add(instance)
        if not open_in_bg:
            self.selected = instance

        return instance

    def check_for_selection(self, event: int) -> None:
        """Handles app selection"""
        
        nothing_zone = self.selected.app.surface.get_surface_range() if not isinstance(self.selected.app, Desktop) else ([0, 0], [0, 0])
        
        if not between(event.pos, *nothing_zone):
            app_instance_choices = list(filter(lambda app_inst, event=event: between(event.pos, *app_inst.app.surface.get_surface_range()), self.running_apps))
            
            # Get surfaces, check it's rank in the render_queue and get the first
            max_index = -1

            def get_index(surface: Surface) -> int:
                return self.system.graphics.conn_pygame_graphics.get_index(surface)

            self.logger.debug(list(map(lambda app_inst: app_inst.app, app_instance_choices)))
            app_surfaces = list(map(lambda app_inst: app_inst.app.surface, app_instance_choices))
            for index, surface in enumerate(app_surfaces):
                gotten_index = get_index(surface)
                if max_index == -1 or gotten_index > get_index(app_surfaces[max_index]):
                    max_index = index
            
            self.selected = app_instance_choices[max_index]
            if not isinstance(self.selected.app, Desktop):
                self.system.graphics.conn_pygame_graphics.select_surface(self.selected.app.surface)
    
    def events_handler(self) -> None:
        """Events handler for the operating system"""
        
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
    
            # Window selection
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.check_for_selection(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                self.start_app(Explorer, self)

    def main_loop(self, clock: pygame.time.Clock, fps: int) -> None:
        """Runs main loop of the Operating System"""

        self.boot()

        while self.running:
            self.system.graphics.render_surfaces()
            if self.temp and self.temp.result():
                self.logger.debug(self.temp.result())
            clock.tick(fps)

            self.events = pygame.event.get()
            
            self.events_handler()
            
            for instance in self.running_apps:
                if not instance.alive:
                    self.running_apps.remove(instance)

            for instance in self.running_apps: 
                if (not instance.running):
                    instance.set_bg(instance != self.selected)

                instance.app.send_events(self.events)
                self.temp = self.executor.submit(instance.run)

            #self.logger.debug(f'Selected {self.selected.app}')