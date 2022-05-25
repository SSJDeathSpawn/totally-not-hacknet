from __future__ import annotations

from typing import TYPE_CHECKING, Optional
import time
import random

import pygame

from game.applications.application import Application
from exceptions.applications import MessageBoxError
from graphics.constants import MESSAGE_BOX_DIMENSIONS, MESSAGE_BOX_PADDING, MESSAGE_BOX_FONT_SIZE, RESOLUTION, MESSAGE_BOX_BGCOLOR, MESSAGE_BOX_OUTLINE_COLOR
from graphics.text import Text
if TYPE_CHECKING:
    from graphics.conn_pygame_graphics import Surface
    from game.operating_system import OperatingSystem


class MessageBox(Application):
    """A messagebox which displays a message for a given amount of time"""

    def __init__(self, host: OperatingSystem, message: str, color: tuple[int, int, int, int], seconds: int, opened_by: Optional[OperatingSystem] = None):
        super().__init__(host, opened_by)

        # self.surface: Surface = self.host.system.graphics.get_surface(*MESSAGE_BOX_DIMENSIONS, [(RESOLUTION[0] - MESSAGE_BOX_DIMENSIONS[0] - 20), (RESOLUTION[1] - MESSAGE_BOX_DIMENSIONS[1] - 20)])
        self.surface: Surface = self.graphics.get_surface(*MESSAGE_BOX_DIMENSIONS, [random.randint(20, RESOLUTION[0] - MESSAGE_BOX_DIMENSIONS[0] - 20), random.randint(20, RESOLUTION[1] - MESSAGE_BOX_DIMENSIONS[1] - 20)])

        self.message: Text = Text(message, color, 'regular', MESSAGE_BOX_FONT_SIZE, (MESSAGE_BOX_PADDING[0], MESSAGE_BOX_PADDING[1]), self.surface.get_width() - (2 * MESSAGE_BOX_PADDING[0]), self.surface.get_height() - (2 * MESSAGE_BOX_PADDING[1]), [0, 0])

        self.graphics.clear_surface(self.surface, MESSAGE_BOX_BGCOLOR)
        self.graphics.display_messagebox_text(self.surface, self.message.get_processed_text(), MESSAGE_BOX_FONT_SIZE, MessageBoxError)

        self.seconds: float = float(seconds)
        self.start_time: float = time.perf_counter()

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:
        self.graphics.clear_surface(self.surface, MESSAGE_BOX_BGCOLOR)
        self.graphics.display_messagebox_text(self.surface, self.message.get_processed_text(), MESSAGE_BOX_FONT_SIZE, MessageBoxError)
        self.graphics.draw_outline(self.surface, MESSAGE_BOX_OUTLINE_COLOR)

    def events_handler(self) -> None:
        for event in self.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit(debug=0)

    def tick(self, bg=False) -> str:
        if time.perf_counter() - self.start_time >= self.seconds:
            self.quit(debug=0)
            return
        super().tick(bg)
