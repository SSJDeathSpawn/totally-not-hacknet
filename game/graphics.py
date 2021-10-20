import pygame

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
        self.conn_pygame_graphics.draw_rect((255, 0, 0), surface.get_width() * (9 / 10), 0, surface.get_width(), surface.get_height() / 10, width=0, surface=surface)
        self.conn_pygame_graphics.draw_rect((155, 155, 155), surface.get_width() * (8 / 10), 0, surface.get_width() / 10, surface.get_height() / 10, width=0, surface=surface)
        self.conn_pygame_graphics.draw_rect(color, 0, surface.get_height() / 10, surface.get_width(), surface.get_height() * (9 / 10), width=0, surface=surface)
        self.conn_pygame_graphics.render_text('bold', surface.get_height() // 20, name, (0, 0, 0), None, (surface.get_width() * (2 / 5), surface.get_height() / 20), surface=surface)
        self.conn_pygame_graphics.push_surface(surface)
        return surface

    def fill_application_window(self, surface, color):
        self.conn_pygame_graphics.draw_rect(color, 0, surface.get_height() / 10, surface.get_width(), surface.get_height() * (9 / 10), width=0, surface=surface)

    def display_terminal_text(self, surface, text):
        text_surface = pygame.Surface((surface.get_width(), surface.get_height() * (9 / 10)), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))

        lines = []

        font_size = text_surface.get_width() // 30
        height = font_size
        width = font_size * 3 / 5
        number_of_characters = text_surface.get_width() // width
        number_of_lines = text_surface.get_height() // height

        count = 0
        newline = ''
        for letter in text:
            if count == number_of_characters:
                count = 0
                lines.append(newline)
                newline = ''
            if letter == '\n':
                count = 0
                lines.append(newline)
                newline = ''
                continue
            newline += letter
            count += 1
        lines.append(newline)

        lines = lines[-number_of_lines:]

        # self.conn_pygame_graphics.render_text('regular', 20, text, (0, 0, 0), None, (0, 0), 0b100000000, text_surface)

        for i in range(len(lines)):
            self.conn_pygame_graphics.render_text('regular', font_size, lines[i], (0, 0, 0), None, (0, i * (font_size - 0.5)), 0b100000000, text_surface)

        surface.blit(text_surface, (0, surface.get_height() / 10))
