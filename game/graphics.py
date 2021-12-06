import pygame

from custom_logging.logging import get_logger
from graphics.conn_pygame_graphics import Surface
from game.constants import *


logger = get_logger('game')


class Graphics(object):
	def __init__(self, conn_pygame_graphics):
		self.conn_pygame_graphics = conn_pygame_graphics

	def get_system_surface(self):
		surface = Surface((self.conn_pygame_graphics.win.get_width(), self.conn_pygame_graphics.win.get_height()), (0, 0))
		self.conn_pygame_graphics.push_surface(surface)
		return surface

	def draw_application_window(self, width, height, color, name, titlebar=True) -> Surface:
		surface = Surface((width, height), ((self.conn_pygame_graphics.win.get_width() - width) / 2, (self.conn_pygame_graphics.win.get_height() - height) / 2))
		surface.fill((0, 0, 0, 0))
		if titlebar:
			self.conn_pygame_graphics.draw_rect((0, 0, 0), 0, 0, surface.get_width(), titlebar_height, width=0, surface=surface)
			self.conn_pygame_graphics.draw_rect((255, 0, 0), surface.get_width() - titlebar_comp_width, 0, titlebar_comp_width, titlebar_height, width=0, surface=surface)
			self.conn_pygame_graphics.draw_rect((155, 155, 155), surface.get_width() - (2 * titlebar_comp_width), 0, titlebar_comp_width, titlebar_height, width=0, surface=surface)
			self.fill_application_window(surface, color)
			self.conn_pygame_graphics.render_text('bold', int(titlebar_height / 2), name, (255, 255, 255), ((surface.get_width() - (2 * titlebar_comp_width)) // 2, titlebar_height // 2), alignment=0b1100, surface=surface)
		self.conn_pygame_graphics.push_surface(surface)
		return surface 
	
	def rendered_icon(self, path_from_res, icon_name, text_colour, font_size, text_gap, height=-1, width=-1, additive=True):
		image = self.conn_pygame_graphics.convert_to_pygame_image(path_from_res)
		icon = Surface(((image.get_width()+20 if width < 0 else width+20), (image.get_height()+30 if height < 0 else height+30)),(0,0))
		image = pygame.transform.scale(image, (width if width > 0 else image.get_width(), height if height > 0 else image.get_height()))
		self.conn_pygame_graphics.blit_image((10, 10), image, height, width, additive, 0b0000, icon)
		self.conn_pygame_graphics.render_text('regular', font_size, icon_name, text_colour, point=(((width+20 if width != -1 else image.get_width()+20)/2), (height+20 if height != -1 else image.get_height()+20)+text_gap), background=None, alignment=0b1000, surface=icon)
		return icon 
	
	def outline_surface(self, surface, colour, thickness):
		return self.conn_pygame_graphics.outline_surface(surface, colour, thickness)

	def fill(self, surface, color):
		self.conn_pygame_graphics.draw_rect(color, 0, 0, surface.get_width(), surface.get_height(), width=0, surface=surface)

	def fill_with_image(self, surface, path_to_img):
		self.conn_pygame_graphics.blit_image((0, 0), self.conn_pygame_graphics.convert_to_pygame_image(path_to_img), alignment=0b0000, surface=surface)

	def fill_application_window(self, surface, color):
		self.conn_pygame_graphics.draw_rect(color, 0, titlebar_height, surface.get_width(), surface.get_height() - titlebar_height, width=0, surface=surface)

	def display_explorer_icons(self, surface, units, icon_dimensions, space, scroll, file_icon_path, folder_icon_path):
		limit = surface.get_width() // (icon_dimensions[0] + space[0])
		new_surface_height = ((icon_dimensions[1] + space[1]) * ((len(units.keys()) // limit) + 1))

		if scroll > (new_surface_height - surface.get_height()):
			scroll = new_surface_height - surface.get_height()

		icons_surface = pygame.Surface((surface.get_width(), new_surface_height), pygame.SRCALPHA)
		icons_surface.fill((0, 0, 0, 0))

	def display_terminal_text(self, surface, text):
		text_surface = pygame.Surface((surface.get_width(), surface.get_height() - titlebar_height), pygame.SRCALPHA)
		text_surface.fill((0, 0, 0, 0))

		for string in text.processed:
			self.conn_pygame_graphics.render_text(string[1], text.get_font_size_scaled(), string[0], string[2], string[3], surface=text_surface)

		surface.blit(text_surface, (0, titlebar_height))
