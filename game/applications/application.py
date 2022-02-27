from __future__ import annotations
from typing import TYPE_CHECKING, Optional, ClassVar
from threading import Thread
from logging_module.custom_logging import get_logger
if TYPE_CHECKING:
    from game.operating_system import OperatingSystem



class Application(object):
    """Class representing an application which is installed in the OS"""
    
    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None):

        if not opened_by:
            opened_by = host

        self.opened_by: OperatingSystem = opened_by
        self.host: OperatingSystem = host
        self.graphics: Any = graphics = self.host.system.graphics  #FIXME: replace Any with the class
    
    def tick(self, bg=False) -> None:
        """A single tick of the application"""
    
        if bg:
            self.idle()
        else:
            self.run()

    def run(self) -> None:
        """Runs the graphics and events handlers"""

        self.graphics_handler()
        self.events_handler()

    def idle(self) -> None:
        """Idle state of the application"""
        
        pass
        
    def events_handler(self) -> None:
        """Handles the pygame events passed into the application on the current tick"""
        
        pass

    def graphics_handler(self) -> None:
        """Calls the pygame graphics functions for the application"""

        pass

class MasterApplication(Application):
    """An application derivative that can make the OS open other applications and allocate new memory to them"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None) -> None:
        super().__init__(host, opened_by)
        
        self.children: set[ApplicationInstance] = set()

    def start_application(self, app_class: ClassVar[Application], open_in_bg: bool = False) -> None:
        """Starts a new application instance on behalf of the host Operating System"""

        instance = self.host.start_app(app_class, self.opened_by, open_in_bg)
        self.children.add(self.host.start_app())


class ApplicationInstance(Thread):
    """A thread-based class which handles the instance of an Application which is an analogue to a running program"""

    def __init__(self, app: Application, pid: int, run_in_bg: bool = False) -> None:

        super().__init__()

        self.logger = get_logger('game')

        self.app: Application = app
        self.pid: int = pid
        self.run_in_bg: bool = run_in_bg
        
        self.running: bool = False
        self.alive: bool = True

    def run(self) -> None:
        """Runs one tick of the application"""

        if self.alive and not self.running:
            self.running = True
            self.app.tick(bg = self.run_in_bg)
            self.running = False

    def terminate(self) -> None:
        """Terminates the application"""
        
        self.alive = False
        self.logger.info(f"Program {self.pid} was terminated")

    def set_bg(self, run_in_bg: bool) -> None:
        """Sets whether the app runs in background or not"""

        self.run_in_bg = run_in_bg
