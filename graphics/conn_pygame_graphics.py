from custom_logging.logging import get_logger
from utils import id_generator
import os

import pygame, math


logger = get_logger('graphics')


class Surface(pygame.Surface):
	"""
	Derives from pygame.Surface and adds ID and pos Attributes.

	Attributes:
		ID - ID of the Surface.
		pos - Position of the Surface on the main display surface.
	"""
	def __init__(self, size, pos):
		"""
		Parameters:
			size - Tuple containing width and height of the Surface. (int width, int height)
		"""
		super().__init__(size, pygame.SRCALPHA)
		self.ID = f'SURFACE-{id_generator.generate_id()}'
		self.pos = pos

		logger.debug(f'Initialized Surface with ID {self.ID} and size ({size[0]}, {size[1]}).')


class ConnPygameGraphics(object):
	"""This class handles the outermost layer of graphics in the Application.

	Attributes:
		width -- width of the pygame window.
		height -- height of the pygame window.
		caption -- caption of the pygame window.
	"""

	def __init__(self, width, height, caption):
		"""
		Parameters:
			width -- width of the pygame window.
			height -- height of the pygame window.
			caption -- caption of the pygame window.
		"""

		pygame.init()

		self.width = width
		self.height = height
		self.caption = caption

		self.first_run = True
		self.win = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.caption)

		self.fps = 30
		self.clock = pygame.time.Clock()

		self.fonts = {
			'regular': 'res/fonts/SourceCodePro-Regular.ttf',
			'bold': 'res/fonts/SourceCodePro-Bold.ttf'
		}

		self.render_queue = []

		logger.info('Initialized Main Graphics API.')

	def main(self, system_id):
		"""Called on every Iteration of the Game Loop."""

		self.clock.tick(self.fps)
		self.win.fill(pygame.Color('black'))
		for surface in self.render_queue:
			if not surface.ID == system_id:	self.win.blit(surface, surface.pos)
		# system = list(filter(lambda s: s.ID == system_id, self.render_queue))[0]
		self.win.blit(system:=list(filter(lambda s: s.ID == system_id, self.render_queue))[0], system.pos) 
		pygame.display.update()

	def push_surface(self, surface):
		"""Push a surface to the queue."""

		self.render_queue.append(surface)
		logger.debug(f'Pushed Surface with ID {surface.ID} to the Render Queue.')

	def pop_surface(self, surface):
		"""Pop a surface from the queue"""

		self.render_queue.remove(surface)
		logger.debug(f'Poped Surface with ID {surface.ID} from the Render Queue.')

	def select_surface(self, surface):
		"""Puts a surface at the bottom of the queue."""

		self.render_queue.remove(surface)
		self.render_queue.append(surface)
		logger.debug(f'Surface with ID {surface.ID} selected.')

	def render_text(self, font_type, size, text, colour, point, background=None, alignment=0b1100, surface=None):
		"""
		Render text on a given Surface.

		Parameters:
			type - Font type (regular, thin, italic, combinations)
			size - Font size
			text - Text to render
			color - Color of the text
			point - Point to align to
			alignment - Where the position is based on (left-top, center-center, bottom-right, etc). A 4 bit number
						Bits:
							1st - Whether x should be centred
							2nd - Whether y should be centred
							3rd - Left or Right (if x is not centred) 
							4th - Top or Bottom (if y is not centred) 
			background - Color of text background. No background if None.
			center -  Center of where to display the text
			surface - Surface to render on
		"""

		surface = surface if surface else self.win
		logger.debug(point)
		try:
			font = pygame.font.Font(self.fonts[font_type], size)
		except KeyError:
			logger.error(f'Invalid Font Type "{font_type}". Ignoring Render Request...')
			return

		#text = font.render(text, False, colour, background) if background else font.render(text, True, colour)
		text = font.render(text, False, colour, background) if background else font.render(text, True, colour)
		text_rect = text.get_rect()


		if alignment & 0b1100: #If both are supposed to be centered
			text_rect.center = point
		elif alignment & 0b100: #If Only y is to be centered
			if alignment & 0b10: #Y center, right
				text_rect.midright = point
			else: #Y center, left
				text_rect.midleft = point
		elif alignment & 0b1000: #If only x is to be centered
			if alignment & 0b1: # X center, down
				text_rect.midbottom = point
			else: #X center, up
				text_rect.midtop = point
		else: #No centered
			if alignment & 0b10: # Right
				if alignment &0b1:
					text_rect.bottomright = point
				else:
					text_rect.topright = point
			else: #Left
				if alignment & 0b1:
					text_rect.bottomleft = point
				else:
					text_rect.topleft = point

		surface.blit(text, text_rect)
	
	def outline_surface(self, surface, colour, outline):
		self.draw_rect(colour, 0, 0, surface.get_width(), surface.get_height(), outline, surface)
		# mask = pygame.mask.from_surface(surface)
		# mask_surf = mask.to_surface(setcolor=colour)
		# mask_surf = pygame.transform.scale(mask_surf, (mask_surf.get_width()+(outline*2), mask_surf.get_height()+(outline*2) ))
		# surf_rect = surface.get_rect()
		# surf_rect.center = (mask_surf.get_width()/2, mask_surf.get_height()/2)
		# mask_surf.blit(surface, surf_rect)
		# return mask_surf

	def convert_to_pygame_image(self, path_from_res):
		image = pygame.image.load(os.path.dirname(os.path.realpath(__file__))+'/../res'+path_from_res)
		return image

	def blit_image(self, pos, image, width=-1, height=-1, additive=True, alignment=0b1100, surface=None):
		"""
		Put an image on a surface at a certain location.

		Args:
			pos - The position where image should be placed
			image - The pygame image object of the image you want to draw
			width - The width of the final image that is to be drawn. -1 means that it will take the width of the image provided.
			height - The height of the final image that is to be drawn. -1 means that it will take the height of the image provided.
			additive - Draws using additive mode and not just putting on top. Defaults to True.
			alignment - Where the position is based on (left-top, center-center, bottom-right, etc). A 4 bit number
						Bits:
							1st - Whether x should be centred
							2nd - Whether y should be centred
							3rd - Left or Right (if x is not centred) 
							4th - Top or Bottom (if y is not centred) 
			surface - The surface to which the image should be drawn to. Defaults to None.
		"""

		#TODO: Add additive and width and height stuff
		surface = surface if surface else self.win
		logger.debug(type(image))
		new_image_size = (width if width > 0 else image.get_width(), height if height>0 else height.get_height())
		image = pygame.transform.scale(image, new_image_size)
		image_rect = image.get_rect()

		if alignment & 0b1100: #If both are supposed to be centered
			image_rect.center = pos
		elif alignment & 0b100: #If Only y is to be centered
			if alignment & 0b10: #Y center, right
				image_rect.midright = pos
			else: #Y center, left
				image_rect.midleft = pos
		elif alignment & 0b1000: #If only x is to be centered
			if alignment & 0b1: # X center, down
				image_rect.midbottom = pos
			else: #X center, up
				image_rect.midtop = pos
		else: #No centered
			if alignment & 0b10: # Right
				if alignment &0b1:
					image_rect.bottomright = pos
				else:
					image_rect.topright = pos
			else: #Left
				if alignment & 0b1:
					image_rect.bottomleft = pos
				else:
					image_rect.topleft = pos
		surface.blit(image, image_rect)


	def draw_rect(self, color, rect_x, rect_y, rect_width, rect_height, width=0, surface=None):
		"""
		Draw a Rectangle on the screen.

		Parameters:
			color - color
			rect_x - x of the rectangle.
			rect_y - y of the rectangle.
			rect_width - width of the rectangle.
			rect_height - height of the rectangle.
			width - width = 0, fill the shape
					width < 0, nothing
					width > 0, fill will be used for
			surface - surface to draw on.
		"""

		surface = surface if surface else self.win
		return pygame.draw.rect(surface, color, pygame.Rect(rect_x, rect_y, rect_width, rect_height), width)

	def draw_polygon(self, color, points, width=0, surface=None):
		"""
		Draw a Polygon on the screen.

		Parameters:
			color - color
			points - List of tuples/lists/pygame.Vector2's holding x and y values for each point of the polygon.
			width - width = 0, fill the shape
					width < 0, nothing
					width > 0, fill will be used for
			surface - surface to draw on.
		"""

		surface = surface if surface else self.win
		return pygame.draw.polygon(surface, color, points, width)

	def draw_circle(self, color, center, radius, quadrants, width=0, surface=None):
		"""
		Draw a Circle on the screen.

		Parameters:
			color - color
			center - tuple/list/vector2 holding x and y values.
			radius - radius of the circle
			quadrants - 0b1000 - Top right
						0b0100 - Top left
						0b0010 - Bottom left
						0b0001 - Bottom right
			width - width = 0, fill the shape
					width < 0, nothing
					width > 0, fill will be used for
			surface - surface to draw on.
		"""

		surface = surface if surface else self.win
		bool_quads = [bool(quadrants & 0b1000), bool(quadrants & 0b100), bool(quadrants & 0b10), bool(quadrants & 0b1)]
		return pygame.draw.circle(surface, color, center, radius, width, *bool_quads)

	def draw_ellipse(self, color, rect_x, rect_y, rect_width, rect_height, width=0, surface=None):
		"""
		Draw an Ellipse on the screen.

		Parameters:
			color - color
			rect_x - x of the rectangle.
			rect_y - y of the rectangle.
			rect_width - width of the rectangle.
			rect_height - height of the rectangle.
			width - width = 0, fill the shape
					width < 0, nothing
					width > 0, fill will be used for
			surface - surface to draw on.
		"""

		surface = surface if surface else self.win
		return pygame.draw.ellipse(surface, color, pygame.Rect(rect_x, rect_y, rect_width, rect_height), width)

	def draw_arc(self, color, rect_x, rect_y, rect_width, rect_height, start_angle, stop_angle, width=1, surface=None):
		"""
		Draw an arc on the screen

		Parameters:
			color - color
			rect_x - x of the rectangle.
			rect_y - y of the rectangle.
			rect_width - width of the rectangle.
			rect_height - height of the rectangle.
			start_angle - starting angle in degrees.
			stop_angle - stopping angle in degrees.
			width - width = 0, nothing will be drawn
					width > 0, (default is 1) used for line thickness
					width < 0, same as width == 0
			surface - surface to draw on.
		"""

		surface = surface if surface else self.win
		return pygame.draw.arc(surface, color, pygame.Rect(rect_x, rect_y, rect_width, rect_height), math.radians(start_angle), math.radians(stop_angle) , width)

	def draw_line(self, color, start_pos, end_pos, width=1, surface=None):
		"""
		Draw a line on the screen.

		Parameters:
			color - color
			start_pos - tuple/list/vector2 holding x and y values.
			end_pos - tuple/list/vector2 holding x and y values.
			width - width = 0, nothing will be drawn
					width > 0, (default is 1) used for line thickness
					width < 0, same as width == 0
			surface - surface to draw on.
		"""

		surface = surface if surface else self.win
		return pygame.draw.line(surface, color, start_pos, end_pos, width)

	def draw_lines(self, color, closed, points, width=1, surface=None):
		"""
		Draw multiple lines on the screen.

		Parameters:
			color - color
			closed - Make a line from start point to end point if True.
			points - List of tuples/lists/pygame.Vector2's holding x and y values for each point to draw.
			width - width = 0, nothing will be drawn
					width > 0, (default is 1) used for line thickness
					width < 0, same as width == 0
			surface - surface to draw on.
		"""

		surface = surface if surface else self.win
		return pygame.draw.lines(surface, color, closed, points, width)
