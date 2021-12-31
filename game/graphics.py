from re import U
import pygame

from custom_logging.logging import get_logger
from game.storage_system import file
from graphics.conn_pygame_graphics import Surface
from game.constants import *
from game.storage_system.file import File


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
		limit = surface.get_width() // (icon_dimensions[0] + (2 * space[0]))
		extra = surface.get_width() - limit * (icon_dimensions[0] + (2 * space[0]))
		new_surface_height = ((icon_dimensions[1] + (3 * space[1])) * ((len(units.keys()) // limit) + 1))

		if scroll > (abs(new_surface_height - surface.get_height())):
			scroll = new_surface_height - surface.get_height()

		icons_surface = pygame.Surface((surface.get_width(), new_surface_height), pygame.SRCALPHA)
		icons_surface.fill((0, 0, 0, 0))

		count = 0

		render_last = None
		# render_last_count = 0
		selected = list(filter(lambda unit: units[unit], units))
		if len(selected) == 1:
			render_last = selected[0]

		for unit in units:
			if unit == render_last: 
				render_last_count = count
				count += 1
				continue
			row = count // limit
			col = count % limit

			if isinstance(unit, File): path = file_icon_path
			else: path = folder_icon_path

			self.display_icon(icons_surface, unit, row, col, icon_dimensions, space, path, units[unit])

			count += 1
	
		if render_last:
			row = render_last_count // limit
			col = render_last_count % limit

			if isinstance(render_last, File): path = file_icon_path
			else: path = folder_icon_path

			self.display_icon(icons_surface, render_last, row, col, icon_dimensions, space, path, units[render_last], full_name=True)

		surface.blit(icons_surface, (extra//2, -scroll))

	def display_icon(self, surface, unit, row, col, icon_dimensions, space, path, selected, full_name=False):
		name = unit.get_name()
		if name == "home":
			name = "asdhasuidahsd asfjhasf sdj sdjhs sjd"
			full_name = True
		x = col * (icon_dimensions[0] + (2 * space[0]))
		y = row * (icon_dimensions[1] + (3 * space[1]))
		name_attr = (space[0] + icon_dimensions[0] / 2, icon_dimensions[1] + space[1] + space[1] / 3)
		fontsize = 12

		if not full_name: name = name[:int((icon_dimensions[0] // (fontsize * 3/5))-2)] + ".." if len(name) > (icon_dimensions[0] // (fontsize * 3/5)) else name

		color = (0, 0, 0, 0) if not selected else (155, 155, 155, 25)

		block = pygame.Surface((icon_dimensions[0] + (2 * space[0]), icon_dimensions[1] + (3 * space[1])), pygame.SRCALPHA)
		block.fill(color)

		image = self.conn_pygame_graphics.convert_to_pygame_image(path)
		image = pygame.transform.scale(image, icon_dimensions)
		
		if not full_name:
			self.conn_pygame_graphics.blit_image(space, image, icon_dimensions[1], icon_dimensions[0], True, 0b0000, block)
			self.conn_pygame_graphics.render_text('regular', fontsize, name, (255, 255, 255), point=name_attr, background=None, alignment=0b1000, surface=block)
		else:
			upperlimit = int(icon_dimensions[0] // (fontsize * 3/5))
			lowerlimit = int(upperlimit * 3/4)
			words = name.split(' ')
			check = words[0]
			count = 0
			lines = []
			while True:
				if count > len(words) - 1: break
				while len(check) <= lowerlimit: # 11
					count += 1
					if count > len(words) - 1: break
					check += " " + words[count]

				if len(check) >= upperlimit+1:
					if check[upperlimit] == " ":
						lines.append(check[:upperlimit])
						check = check[upperlimit+1:]

					elif check[upperlimit-1] == " ":
						lines.append(check[:upperlimit-1])
						check = check[upperlimit:]
					
					elif check[upperlimit-2] == " ":
						lines.append(check[:upperlimit-2])
						check = check[upperlimit-1:]
					
					else:
						lines.append(check[:upperlimit-1] + "-")
						check = "-" + check[upperlimit-1:]

				else:
					lines.append(check)
					check = ""
					
			extra = len(lines) * fontsize
			block = pygame.Surface((icon_dimensions[0] + (2 * space[0]), icon_dimensions[1] + (3 * space[1]) + extra), pygame.SRCALPHA)
			block.fill(color)

			self.conn_pygame_graphics.blit_image(space, image, icon_dimensions[1], icon_dimensions[0], True, 0b0000, block)

			text_y = name_attr[1]
			for line in lines:
				self.conn_pygame_graphics.render_text('regular', fontsize, line, (255, 255, 255), point=(name_attr[0], text_y), background=None, alignment=0b1000, surface=block)
				text_y += fontsize

		surface.blit(block, (x, y))

	def display_terminal_text(self, surface, text):
		text_surface = pygame.Surface((surface.get_width(), surface.get_height() - titlebar_height), pygame.SRCALPHA)
		text_surface.fill((0, 0, 0, 0))

		for string in text.processed:
			self.conn_pygame_graphics.render_text(string[1], text.get_font_size_scaled(), string[0], string[2], string[3], surface=text_surface)

		surface.blit(text_surface, (0, titlebar_height))
