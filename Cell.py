"""Cell object in the 2-d list grid system"""
import pygame
from Constants import *
from Wall import *


class Cell(pygame.sprite.Sprite):
    """
    each cell has four wall objects
    for path finding: each cell has a list of child list that contains all the approachable cell from self
    """

    def __init__(self, x, y, screen):
        """construct the cell with four wall objects according the position of the cell from <x> and <y>
        @type x: this is the top left x_cor on the screen
        @type y: this is the top right x_cor on the screen
        """
        super().__init__()

        self.image = pygame.Surface([WALL_LENGTH, WALL_LENGTH])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        # set the top left of the cell
        self.rect.x, self.rect.y = x, y
        # get the center position of the cell
        self.center = self.rect.center

        self.visited = False  # if visited, return True for maze algorithm
        self.tree_visited = False  # for construct tree use 

        self.top_wall = Wall([x, y], [x + WALL_LENGTH, y], screen)
        self.left_wall = Wall([x, y], [x, y + WALL_LENGTH], screen)
        self.bottom_wall = Wall([x, y + WALL_LENGTH], [x + WALL_LENGTH, y + WALL_LENGTH], screen)
        self.right_wall = Wall([x + WALL_LENGTH, y], [x + WALL_LENGTH, y + WALL_LENGTH], screen)

        # a list of neighbour objects
        self.neighbour_cells = {'top': None, 'right': None, 'bottom': None, 'left': None}
        self.screen = screen

        # all the available cells from self for the maze
        self.adjacent_cells = []

        self.id = None  # (0, 2) ex
        self.str_id = None  # a string '02' ex

    def set_id(self, x, y):
        self.id = (x, y)
        self.str_id = str(x) + str(y)
    
    def set_color(self, color):
        self.image.fill(color)
    
    def reset_tree_props(self):
        """reset the properties that are used to generate a tree map"""
        self.set_color(BLACK)
        self.tree_visited = False
        self.adjacent_cells = []

    def __repr__(self):
        return self.str_id
