from __future__ import annotation
from typing import TYPE_CHECKING
from logging_module.custom_logging import get_logger
from graphics.conn_pygame_graphics import ConnPygameGraphics
if TYPE_CHECKING:
    from logging import Logger
    from game.system import System


class Graphics(object):
    """System graphics layer"""

    def __init__(self, system: System) -> None:
        self.logger: Logger = get_logger('graphics')
        self.system: System = system

        self.conn_pygame_graphics: ConnPygameGraphics = ConnPygameGraphics()

    def draw_image(self) -> None:  # Subject to change
        pass

    def draw_desktop_icon(self) -> None:  # Subject to change
        pass
