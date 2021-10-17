from custom_logging.logging import get_logger
from utils import id_generator

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
        super().__init__(size)
        self.ID = f'SURFACE-{id_generator.generate_id()}'
        self.pos = pos

        logger.debug(f'Initialized Surface with ID {self.ID} and size ({size[0]}, {size[1]}).')


class ConnPygameGraphics(object):
    """
    This class handles the outermost layer of graphics in the Application.
    """

    def __init__(self, width, height, caption):
        """
        Parameters:
            width - width of the pygame window.
            height - height of the pygame window.
            caption - caption of the pygame window.
        """

        pygame.init()

        self.width = width
        self.height = height
        self.caption = caption

        self.first_run = False

        self.fps = 30
        self.clock = pygame.time.Clock()

        self.fonts = {
            'regular': 'res/fonts/SourceCodePro-Regular.ttf',
            'bold': 'res/fonts/SourceCodePro-Bold.ttf'
        }

        self.render_queue = []

        logger.info('Initialized Main Graphics API.')

    def main(self):
        """Called on every Iteration of the Game Loop."""

        if not self.first_run:
            self.first_run = True
            self.win = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption(self.caption)

        self.clock.tick(self.fps)
        self.win.fill(pygame.Color('black'))
        for surface in self.render_queue:
            self.win.blit(surface, surface.pos)
        pygame.display.update()

    def push_surface(self, surface):
        """Push a surface to the Stack."""

        self.render_queue.append(surface)
        logger.debug(f'Pushed Surface with ID {surface.ID} to the Render Stack.')

    def pop_surface(self, surface):
        """Pop a surface from the stack"""

        self.render_queue.pop(surface)
        logger.debug(f'Poped Surface with ID {surface.ID} from the Render Stack.')

    def render_text(self, font_type, size, text, color, background, center, surface=None):
        """
        Render text on a given Surface.

        Parameters:
            type - Font type (regular, thin, italic, combinations)
            size - Font size
            text - Text to render
            color - Color of the text
            background - Color of text background. No background if None.
            center -  Center of where to display the text
            surface - Surface to render on
        """

        surface = surface if surface else self.win

        try:
            font = pygame.font.Font(self.fonts[font_type], size)
        except KeyError:
            logger.error(f'Invalid Font Type "{font_type}". Ignoring Render Request...')
            return

        text = font.render(text, True, color, background=background) if background else font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = center
        surface.blit(text, text_rect)


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
