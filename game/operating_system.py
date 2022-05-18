from __future__ import annotations

from typing import TYPE_CHECKING, Type, Optional
from concurrent.futures import ThreadPoolExecutor
if TYPE_CHECKING:
    from logging import Logger

import pygame.event
import pygame.time

from logging_module.custom_logging import get_logger
from utils.general_utils import generate_pid
from utils.math import between
from utils.deserializer import deserialize_root_directory
from game.command import Response, Command
from game.storage_system.directory import RootDir, Directory
from game.applications.application import Application, ApplicationInstance
from game.applications.desktop import Desktop
from game.applications.explorer import Explorer
from game.applications.terminal import Terminal
from game.applications.messagebox import MessageBox
from game.constants import APPLICATIONS, DEFAULT_ROOTDIR_PATH
from graphics.constants import MESSAGE_BOX_TEXT_COLOR, MESSAGE_BOX_TIME
from exceptions.storage_system import PathError
from commands.basic import ls, cd, exit_, cat, mkdir, touch, mv, clear
if TYPE_CHECKING:
    from game.system import System
    from game.storage_system.storage_unit import StorageUnit
    from game.storage_system.directory import Directory
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
            Terminal: False,
            Explorer: False
        }

        self.commands = {
            'ls': Command('ls', ls, ''),
            'cd': Command('cd', cd, ''),
            'exit': Command('exit', exit_, ''),
            'cat': Command('cat', cat, ''),
            'mkdir': Command('mkdir', mkdir, ''),
            'touch': Command('touch', touch, ''),
            'mv': Command('mv', mv, ''),
            'clear': Command('clear', clear, '')
            # TODO: Put man entires as constants later on
        }

        self.command_backlog: list[str] = []

        self.selected: ApplicationInstance

        # self.executor: ThreadPoolExecutor = ThreadPoolExecutor()
        self.temp = None

    # Helpers
    def move_to_new_dir(self, su: StorageUnit, new_parent: Directory) -> None:
        """Moves a storage unit from it's current parent to a new directory"""

        su.get_parent().delete(su)
        su.set_parent(new_parent)
        new_parent.add(su)

    def path_exists(self, path: str, current_dir: Directory) -> bool:
        """Returns True if a path exists"""

        try:
            self.get_su_by_path(path, current_dir)
        except PathError:
            return False
        else:
            return True

    def get_app_inst_by_surface(self, surface: Surface) -> Optional[ApplicationInstance]:
        """Returns an application instance by the surface (didn't see this one coming)"""

        try:
            return list(filter(lambda inst: inst.app.surface.ID == surface.ID, self.running_apps))[0]
        except IndexError:
            return

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

        return self.commands.get(name)(app, *args)

    def send_message(self, message: str, color: tuple[int, int, int, int], seconds: int) -> None:
        """Sends a message to the user through a MessageBox"""

        self.start_app(MessageBox, self, False, message, color, seconds)

    def boot(self) -> None:
        """Boots up the Operating System"""
        
        for app in self.startup_apps:
            self.start_app(app, self, self.startup_apps.get(app))

        self.send_message('WELCOME!!!', MESSAGE_BOX_TEXT_COLOR, MESSAGE_BOX_TIME)

    def start_app(self, app: Type[Application], opened_by: OperatingSystem, open_in_bg: bool = False, *args) -> ApplicationInstance:
        """Starts a new application instance"""

        instance = ApplicationInstance(app(self, *args, opened_by=opened_by), generate_pid(), open_in_bg)

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
                # self.executor.shutdown(wait=True)
                pygame.quit()
                return
    
            # Window selection
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.check_for_selection(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                self.start_app(Explorer, self)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.send_message('This is a message box. There is a new message for you.', MESSAGE_BOX_TEXT_COLOR, 10)

    def main_loop(self, clock: pygame.time.Clock, fps: int) -> None:
        """Runs main loop of the Operating System"""

        self.boot()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            while self.running:
                self.system.graphics.render_surfaces()
                if self.temp and self.temp.result():
                    self.logger.debug(self.temp.result())
                clock.tick(fps)

                self.events = pygame.event.get()
                
                self.events_handler()
                if not self.running:
                    break


                for instance in self.running_apps:
                    if not instance.alive:
                        self.running_apps.remove(instance)

                for instance in self.running_apps: 
                    if (not instance.running):
                        instance.set_bg(instance != self.selected)

                    instance.app.send_events(self.events)
                    self.temp = executor.submit(instance.run)

                #self.logger.debug(f'Selected {self.selected.app}')
            
