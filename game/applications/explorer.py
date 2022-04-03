from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from game.applications.application import Application
from graphics.conn_pygame_graphics import Surface
if TYPE_CHECKING:
    from game.operating_system import OperatingSystem


class Explorer(Application):
    """Class representing the file explorer"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None):
        super().__init__(host, opened_by)

        self.surface: Surface = self.host.system.graphics.get_app_surface(800, 600, [200, 200])

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:
        self.graphics.clear_app_surface(self.surface)