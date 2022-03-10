from typing import Optional
from game.applications.application import Application
from game.operating_system import OperatingSystem
from graphics.conn_pygame_graphics import Surface


class Explorer(Application):
    """Class representing the file explorer"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None):
        super().__init__(host, opened_by)

        # self.surface: Surface = self.host.system.graphics.get_surface()
