from custom_logging.logging import get_logger
from graphics.conn_pygame_graphics import Surface


logger = get_logger('game')


class Graphics(object):
    def __init__(self, conn_pygame_graphics):
        self.conn_pygame_graphics = conn_pygame_graphics

    def draw_system_borders(self):
        surface = Surface((self.conn_pygame_graphics.width, self.conn_pygame_graphics.height), (0, 0))
        surface.fill((0, 0, 0, 0))
        self.conn_pygame_graphics.draw_rect((0, 255, 0), 5, 5, surface.get_width() - 10, surface.get_height() - 10, width=1, surface=surface)
        self.conn_pygame_graphics.push_surface(surface)
        return surface

    def draw_application_window(self, width, height, color, name):
        surface = Surface((width, height), ((self.conn_pygame_graphics.width - width) / 2, (self.conn_pygame_graphics.height - height) / 2))
        surface.fill((0, 0, 0, 0))
        self.conn_pygame_graphics.draw_rect((255, 255, 255), 0, 0, surface.get_width(), surface.get_height() / 10, width=0, surface=surface)
        self.conn_pygame_graphics.draw_rect(color, surface.get_width() * (9 / 10), 0, surface.get_width(), surface.get_height() / 10, width=0, surface=surface)
        self.conn_pygame_graphics.draw_rect((155, 155, 155), surface.get_width() * (8 / 10), 0, surface.get_width() / 10, surface.get_height() / 10, width=0, surface=surface)
        self.conn_pygame_graphics.draw_rect((0, 255, 0, 55), 0, surface.get_height() / 10, surface.get_width(), surface.get_height() * (9 / 10), width=0, surface=surface)
        self.conn_pygame_graphics.render_text('bold', surface.get_height() // 20, name, (0, 0, 0), None, (surface.get_width() * (2 / 5), surface.get_height() / 20), surface=surface)
        self.conn_pygame_graphics.push_surface(surface)
        return surface

    def fill_application_window(self, surface, color):
        self.conn_pygame_graphics.draw_rect(color, surface.get_width() * (9 / 10), 0, surface.get_width(), surface.get_height() / 10, width=0, surface=surface)
