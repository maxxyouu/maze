import pygame
from Constants import *

class Player(pygame.sprite.Sprite):
    """a player object that is controlled by the player"""
    
    size = WALL_LENGTH - 1
    def __init__(self, grid):
        """
        @type grid: a maze grid that has tunnel
        """
        super().__init__()
        
        self.image = pygame.Surface([self.size, self.size]).convert()
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.rect.x, self.rect.y = (1, 1)
        # center position of the player
        self.center = self.rect.center

        self.x_speed = 0
        self.y_speed = 0

        # use this as a movement
        self.reference_grid = grid
        self.relative_grid_position = [0, 0]

        # the wall group that the player collide with
        self.walls = pygame.sprite.Group()
        self.target = None

    def horizontal_movement_handler(self, x):
        """handle collision and horizontal movements logics"""

        new_x = self.relative_grid_position[0] + x
        ori_y = self.relative_grid_position[1]
        cell = self.reference_grid[self.relative_grid_position[0]][self.relative_grid_position[1]]

        if 0 <= new_x <= len(self.reference_grid):  # boundaries conditions
            # wall conditions
            if x < 0:
                if not cell.left_wall.draw:
                    self.relative_grid_position = [new_x, ori_y]
            elif x > 0 and new_x >= 0:
                if not cell.right_wall.draw:
                    self.relative_grid_position = [new_x, ori_y]
    
    def vertical_movement_handler(self, y):
        """handle collision and vertical movements logics"""

        ori_x = self.relative_grid_position[0]
        new_y = self.relative_grid_position[1] + y
        cell = self.reference_grid[self.relative_grid_position[0]][self.relative_grid_position[1]]

        if 0 <= new_y <= len(self.reference_grid[self.relative_grid_position[0]]): # boundaries conditions
            # wall conditions
            if y < 0:
                if not cell.top_wall.draw:
                    self.relative_grid_position = [ori_x, new_y]
            elif y > 0:
                if not cell.bottom_wall.draw:
                    self.relative_grid_position = [ori_x, new_y]

    def collide_target(self):
        """assume target is not None"""
        if pygame.sprite.collide_rect(self, self.target):
            self.target.kill()

    def update(self):
        """update the position of the player and handle player collision logics"""

        # move to the cell position
        cell = self.reference_grid[self.relative_grid_position[0]][self.relative_grid_position[1]]
        
        self.rect.x = cell.rect.x
        self.rect.y = cell.rect.y

        self.collide_target()


class Destination(pygame.sprite.Sprite):
    """object that the player need to collide with"""

    size = WALL_LENGTH - 1

    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.image = pygame.Surface([self.size, self.size])
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x, self.rect.y = pos_x, pos_y