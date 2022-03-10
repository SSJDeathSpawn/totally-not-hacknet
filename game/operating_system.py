from __future__ import annotations
from typing import TYPE_CHECKING, Type
from logging import Logger
from logging_module.custom_logging import get_logger
from concurrent.futures import ThreadPoolExecutor
from utils.general_utils import generate_pid
from game.storage_system.directory import RootDir
from game.applications.desktop import Desktop
from game.constants import APPLICATIONS
from game.applications.application import Application, ApplicationInstance
if TYPE_CHECKING:
    from game.system import System

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
        }

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

        return instance

    def main_loop(self, clock: pygame.time.Clock, fps: int) -> None:
        """Runs main loop of the Operating System"""

        self.boot()

        while self.running:
            self.system.graphics.render_surfaces()
            # if self.temp:
                # self.logger.debug(self.temp.result())
            clock.tick(fps)

            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
            
            for instance in self.running_apps:
                if not instance.alive:
                    self.running_apps.remove(instance)

            for instance in self.running_apps:
                if not instance.running:
                    instance.app.send_events(self.events)
                    self.temp = self.executor.submit(instance.run)
