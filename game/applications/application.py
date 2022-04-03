from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Type, Any
from graphics.conn_pygame_graphics import Surface
from graphics.constants import RESOLUTION, TITLEBAR_DEFAULT_HEIGHT, TITLEBAR_OPTIONS_DIMENSIONS
from threading import Thread
from logging_module.custom_logging import get_logger
from utils.math import between, clamp
if TYPE_CHECKING:
    from game.operating_system import OperatingSystem
    from game.graphics import Graphics
    from logging import Logger

import pygame.event
import pygame
import functools
import time


class Application(object):
    """Class representing an application which is installed in the OS"""
    
    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None):
        
        self.logger: Logger = get_logger('game')

        if not opened_by:
            opened_by = host

        self.opened_by: OperatingSystem = opened_by
        self.host: OperatingSystem = host
        self.graphics: Graphics = self.host.system.graphics
        self.events: list[pygame.event.Event] = []
        self.surface: Optional[Surface] = None
        self.copy_surface: Optional[Surface] = None

        self.debug = {
            'i': 0,
            'time': [0,0]
        }

        self.selected: bool = False
        self.is_being_moved: bool = False

    def send_events(self, events: list[pygame.event.Event]):
        """Sends events from the operating system to the application"""

        self.events = events
    
    def tick(self, bg=False) -> str:
        """A single tick of the application"""
    
        if bg:
            self.idle()
        else:
            self.run()

    def run(self) -> None:
        """Runs the graphics and events handlers"""
            
        if self.debug.get('i') >= 99:
            self.logger.debug(f"Average in 100 cycles for {self.__class__.__name__}:")
            self.logger.debug(f"Graphics: {self.debug.get('time')[0] / 100}")
            self.logger.debug(f"Events: {self.debug.get('time')[1] / 100}")
            self.debug['i'] = 0
            self.debug['time'] = [0, 0]

        start = time.time()
        self.graphics_handler()
        end = time.time()
        self.debug['time'][0] += end-start
        start = time.time()
        self.events_handler()
        end = time.time()
        self.debug['time'][1] += end-start
        self.debug['i'] += 1

    def idle(self) -> None:
        """Idle state of the application"""
        
        self.graphics_handler()
    
    def quit(self) -> None:
        """Quits the application"""
        
        self.logger.debug('QUITTING')
        
        self.graphics.remove_surface(self.surface)
        app_to_remove = list(filter(lambda app_instance: app_instance.app == self, self.host.running_apps))[0]
        self.host.running_apps.remove(app_to_remove)

    def events_handler(self) -> None:
        """Handles the pygame events passed into the application on the current tick"""


        for event in self.events:

            if event.type == pygame.MOUSEBUTTONDOWN:  
                #self.logger.debug(f'I\'m pressing the mouse, and I\'m checking if {event.pos} is in between {((self.surface.pos[0] + self.surface.get_width()) - (TITLEBAR_OPTIONS_DIMENSIONS[0] * TITLEBAR_DEFAULT_HEIGHT), self.surface.pos[1])} and {(self.surface.pos[0] + self.surface.get_width(), self.surface.pos[1]+TITLEBAR_DEFAULT_HEIGHT)}')

                # Enables moving the window
                if event.button == 1 and between(event.pos, self.surface.pos, (self.surface.pos[0] + self.surface.get_width() - TITLEBAR_OPTIONS_DIMENSIONS[0] * TITLEBAR_DEFAULT_HEIGHT * 2, self.surface.pos[1] + TITLEBAR_DEFAULT_HEIGHT)):
                    self.is_being_moved = True

                # Quitting the window
                elif event.button == 1 and between(event.pos, (self.surface.pos[0] + self.surface.get_width() - TITLEBAR_OPTIONS_DIMENSIONS[0] * TITLEBAR_DEFAULT_HEIGHT, self.surface.pos[1]), (self.surface.pos[0] + self.surface.get_width(), self.surface.pos[1]+TITLEBAR_DEFAULT_HEIGHT)):
                    self.quit()
                    return

            # Disables moving the window
            if event.type == pygame.MOUSEBUTTONUP and self.is_being_moved:
                self.is_being_moved = False

            # Moves the window with mouse
            if event.type == pygame.MOUSEMOTION and self.is_being_moved:
                self.surface.pos = [clamp(self.surface.pos[0] + event.rel[0], 0 - self.surface.get_width() + 10, RESOLUTION[0] - 10), clamp(self.surface.pos[1] + event.rel[1], 0, RESOLUTION[1] - TITLEBAR_DEFAULT_HEIGHT)]
    
    def graphics_wrapper(func):
        """Wrapper for the graphics handler"""
        
        @functools.wraps(func)
        def wrap(self):
            self.surface = self.graphics.swap_surfaces(self.surface)
            func(self)

        return wrap

    
    @graphics_wrapper
    def graphics_handler(self) -> None:
        """Calls the pygame graphics functions for the application"""

        pass


    graphics_wrapper = staticmethod(graphics_wrapper)


class MasterApplication(Application):
    """An application derivative that can make the OS open other applications and allocate new memory to them"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None) -> None:
        super().__init__(host, opened_by)
        
        self.children: set[ApplicationInstance] = set()

    def start_application(self, app_class: Type[Application], open_in_bg: bool = False) -> None:
        """Starts a new application instance on behalf of the host Operating System"""

        instance = self.host.start_app(app_class, self.opened_by, open_in_bg)
        self.children.add(instance)

    def events_handler(self):
        # Duh, we don't want desktop to be moved around
        pass


class ApplicationInstance(object):
    """A thread-based class which handles the instance of an Application which is an analogue to a running program"""

    def __init__(self, app: Application, pid: int, run_in_bg: bool = False) -> None:

        super().__init__()

        self.logger: Logger = get_logger('game')

        self.app: Application = app
        self.pid: int = pid
        self.run_in_bg: bool = run_in_bg
        
        self.running: bool = False
        self.alive: bool = True

    def run(self) -> None:
        """Runs one tick of the application"""

        if self.alive and not self.running:
            self.running = True
            self.app.tick(self.run_in_bg)
            self.running = False

    def terminate(self) -> None:
        """Terminates the application"""
        
        self.alive = False
        self.logger.info(f"Program {self.pid} was terminated")

    def set_bg(self, run_in_bg: bool) -> None:
        """Sets whether the app runs in background or not"""

        self.run_in_bg = run_in_bg
