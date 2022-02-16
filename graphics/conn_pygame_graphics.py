import pygame

from typing import Optional
from logging_module.custom_logging import get_logger
from utils.general_utils import generate_id
from graphics.constants import *


class Surface(pygame.Surface):
    """Adds ID and pos attributes to the pygame Surface class"""

    def __init__(self, size: tuple[int, int], pos: list[int, int]) -> None:
        
        super().__init__(size, pygame.SRCALPHA)

        self.ID: str = f'SURFACE-{generate_id()}'
        self.pos: list[int, int] = pos


class ConnPygameGraphics(object):
    """Graphics handler at the outermost level"""

    def __init__(self, width: int, height: int, caption: str, fps: int = 30) -> None:  

        self.logger = get_logger('graphics')
        self.logger.info('Hello from ConnPygameGraphics!')

        pygame.init()

        self.width: int = width
        self.height: int = height
        self.caption: int = caption

        self.window: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

        self.fps: int = fps
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.fonts: dict[str, str] = {}
        self.render_queue: list = []

        self.image_path: str = IMAGE_PATH

    # Main

    def main(self) -> None:
        """Called on every iteration of the Game Loop"""

        self.clock.tick(self.fps)

        self.window.fill((0, 0, 0))

        for surface in self.render_queue:
            self.window.blit(surface, surface.pos)

        pygame.display.update()

    # Queue Operations

    def push_surface(self, surface: Surface) -> None:
        """Pushes a surface to the render queue"""

        self.render_queue.append(surface)

    def pop_surface(self) -> Surface:
        """Pops a surface from the render queue"""

        return self.render_queue.pop(0)

    def remove_surface(self, surface: Surface) -> None:
        """Removes a specific surface from the render queue"""

        self.render_queue.remove(surface)

    def select_surface(self, surface: Surface) -> None:
        """Puts a render surface at the end of the queue"""

        self.render_queue.remove(surface)
        self.render_queue.append(surface)

    # Shapes

    def draw_line(self, color: tuple[int, int, int, int], start: tuple[int, int], end: tuple[int, int], width: int = 1, surface: Optional[Surface] = None) -> pygame.Rect:
        """Draws a line of given width (default 1) on a surface (default main window surface)"""

        if not surface:
            surface = self.window

        return pygame.draw.line(surface, color, start, end, width)

    def draw_lines(self, color: tuple[int, int, int, int], points: list[tuple[int, int]], width: int = 1, closed: bool = False, surface: Optional[Surface] = None) -> pygame.Rect:
        """Draws multiple lines on the screen with given width (default 1) connecting all the points in the given sequence on a surface (default main window surface)"""

        if not surface:
            surface = self.window

        return pygame.draw.lines(surface, color, closed, points, width)

    def draw_circle(self, color: tuple[int, int, int, int], center: tuple[int, int], radius: int, quadrants: int = 0b1111, width: int = 0, surface: Optional[Surface] = None) -> pygame.Rect:
        """Draws the specified quadrants of the circle (default 0b1111) on a surface (default main window surface)"""

        if not surface:
            surface = self.window

        quadrants = [bool(quadrants & 0b1000), bool(quadrants & 0b100), bool(quadrants & 0b10), bool(quadrants & 0b1)]

        return pygame.draw.circle(surface, color, center, radius, width, *quadrants)

    def draw_rect(self, color: tuple[int, int, int, int], rect_x: int, rect_y: int, rect_width: int, rect_height: int, width: int = 0, surface: Optional[Surface] = None) -> pygame.Rect:
        """Draws a rectangle with given dimensions on a surface (default main window surface)"""

        if not surface:
            surface = self.window

        return pygame.draw.rect(surface, color, pygame.Rect(rect_x, rect_y, rect_width, rect_height), width)

    def draw_polygon(self, color: tuple[int, int, int, int], points: list[tuple[int, int]], width: int = 0, surface: Optional[Surface] = None) -> pygame.Rect:
        """Draws a polygon using the given points on a surface (defualt main window surface)"""

        if not surface:
            surface = self.window

        return pygame.draw.polygon(surface, color, points, width)

    # Images

    def convert_to_pygame_image(self, name: str) -> pygame.Surface:
        """Loads and returns a pygame image with given name"""

        try:
            image = pygame.image.load(f'{self.image_path}{name}')
        except FileNotFoundError:
            self.logger.error('Invalid image file name. Ignoring load request')
            return

        return image

    def blit_image(self, pos: tuple[int, int], image_name: str, width: int = 0, height: int = 0, surface: Optional[Surface] = None) -> pygame.Rect:
        """Blits an image to a surface (default main window surface)"""

        if not surface:
            surface = self.window

        image = self.convert_to_pygame_image(image_name)

        image_size = (
            width if width > 0 else image.get_width(),
            height if height > 0 else image.get_height()
        )

        image = pygame.transform.scale(image, image_size)
        
        return surface.blit(image, pos)

    # Text

    def render_text(self, font_type: str, size: int, text: str, color: tuple[int, int, int, int], pos: tuple[int, int], background: Optional[tuple[int, int, int, int]] = None, surface: Optional[Surface] = None) -> pygame.Rect:
        """Renders text on a surface (default main window surface)"""

        if not surface:
            surface = self.window

        try:
            font = pygame.font.Font(self.fonts[font_type], size)
        except KeyError:
            self.logger.error(f'Invalid font type {font_type}. Ignoring render request')
            return

        text = font.render(text, False, color, background)

        return surface.blit(text, pos)
