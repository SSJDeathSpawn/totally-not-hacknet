from __future__ import annotations
from typing import TYPE_CHECKING, Type
from logging import Logger
from logging_module.custom_logging import get_logger
from concurrent.futures import ThreadPoolExecutor
from utils.general_utils import generate_pid
from utils.math import between, clamp
from game.storage_system.directory import RootDir
from game.applications.desktop import Desktop
from game.applications.explorer import Explorer
from game.constants import APPLICATIONS
from game.applications.application import Application, ApplicationInstance
if TYPE_CHECKING:
    from game.system import System
    from graphics.conn_pygame_graphics import Surface

import pygame.event
import pygame.time


class OperatingSystem(object):
    """Class representing an Operating System"""
    
    def __init__(self, system: System, root: RootDir) -> None:
        
        self.logger: Logger = get_logger('game')
        self.system: System = system
        self.root: RootDir = root

        self.events: list[pygame.event.Event] = []

        self.installed_apps: dict[str, Type[Application]] = APPLICATIONS

        self.running = True
        self.running_apps: set[ApplicationInstance] = set()

        self.startup_apps: dict[Application, bool] = {
            # class: is_bg
            Desktop: False,
            Explorer: False
        }

        self.selected: ApplicationInstance

        self.executor: ThreadPoolExecutor = ThreadPoolExecutor()
        self.temp = None

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
            if self.temp and self.temp.result() != None:
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