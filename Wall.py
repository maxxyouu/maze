import pygame
from Constants import *

class Wall(pygame.sprite.Sprite):
    """A rectangle object act as a wall"""

    def __init__(self, start_pos, end_pos, screen):
        """rectangle object
        @type start_pos and end_pos: position of the wall line <tuple>
        @type screen: reference screen that the wall being draw on
        """
        super().__init__()

        # line properties
        self.width = 1
        self.length = WALL_LENGTH
        self.color = WHITE

        self.image = self._wall_orientation_image(start_pos, end_pos)
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_pos

        self.start_pos = start_pos
        self.end_pos = end_pos
    
        self.screen = screen

        self.draw = True  # this determine to draw the wall
    
    def _wall_orientation_image(self, begin_pos, end_pos):
        """determine the orientation of the wall and return the image"""
        if begin_pos[0] == end_pos[0]:
            # vertical wall
            return pygame.Surface([self.width, self.length]).convert()
        else:
            # horizontal wall
            return pygame.Surface([self.length, self.width]).convert()