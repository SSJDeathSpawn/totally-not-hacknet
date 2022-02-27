from __future__ import annotations
from typing import TYPE_CHECKING, Type
from logging import Logger
from logging_module.custom_logging import get_logger
from concurrent.furtures import ThreadPoolExecutor
from utils.utils.general_utils import generate_pid
from game.storage_system.directory import RootDir
from game.applications.desktop import DesktopManager
from game.constants import APPLICATIONS
if TYPE_CHECKING:
    import pygame.time

    from game.system import System
    from game.applications.application import Application, MasterApplication, ApplicationInstance


class OperatingSystem(object):
    """Class representing an Operating System"""
    
    def __init__(self, system: System, root: RootDir) -> None:
        
        self.logger: Logger = get_logger('game')
        self.system: System = system
        self.root: RootDir = root

        self.installed_apps: dict[str, Type[Application]] = APPLICATIONS

        self.running_apps: set[ApplicationInstance] = set()

        self.startup_apps: dict[Application, bool] = [  
            # class: is_bg
            DesktopManager: False
        ]

        self.executor: ThreadPoolExecutor = ThreadPoolExecutor()

    def boot(self) -> None:
        """Boots up the Operating System"""
        
        for app in self.startup_apps:
            self.running_apps.add(self.start_app(app, self, self.startup_apps.get(app)))

    def start_app(self, app: Type[Application], opened_by: OperatingSystem, open_in_bg: bool = False) -> ApplicationInstance:
        """Starts a new application instance"""

        instance = ApplicationInstance(app(self, opened_by=opened_by), generate_pid(), open_in_bg)
        self.running_apps.add(instance)

        return instance

    def main_loop(self, clock: pygame.time.Clock, fps: int) -> None:
        """Runs main loop of the Operating System"""
        
        while self.running:
            clock.tick(fps)
            
            for instance in self.running_apps:
                if not instance.alive:
                    self.running_apps.remove(instance)

            for instance in self.running_apps:
                self.executor.submit(instance.run)
