""" player object in the maze(red square) """
import pygame
from Constants import *


class Player(pygame.sprite.Sprite):
    """a player object that is controlled by the player"""
    
    size = WALL_LENGTH - (WALL_LENGTH * 0.2)

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

        # use this as a movement
        self.reference_grid = grid
        self.relative_grid_position = [0, 0]

        # the target that the player collides with, initialize in Game_controller.py
        self.target = None

    def _get_cell_from_grid(self):
        # get the cell object from self.reference_grid
        return self.reference_grid[self.relative_grid_position[0]][self.relative_grid_position[1]]

    def horizontal_movement_handler(self, x):
        """
        1. handle collisions
        2. place the relative_grid_position into a new cell position
        @type x: int speed of the player
        """
        # new cell position
        new_x = self.relative_grid_position[0] + x
        ori_y = self.relative_grid_position[1]
        # original cell position
        cell = self._get_cell_from_grid()

        if 0 <= new_x <= len(self.reference_grid):  # boundaries conditions
            # wall conditions
            if x < 0 and not cell.left_wall.draw_to_screen:
                self.relative_grid_position = [new_x, ori_y]
            elif x > 0 and not cell.right_wall.draw_to_screen:
                self.relative_grid_position = [new_x, ori_y]
    
    def vertical_movement_handler(self, y):
        """
        1. handle collisions
        2. place the relative_grid_position into a new cell position
        @type y: int speed of the player
        """
        # new cell position
        ori_x = self.relative_grid_position[0]
        new_y = self.relative_grid_position[1] + y
        # original cell position
        cell = self._get_cell_from_grid()

        if 0 <= new_y <= len(self.reference_grid[self.relative_grid_position[0]]): # boundaries conditions
            # wall conditions
            if y < 0 and not cell.top_wall.draw_to_screen:
                self.relative_grid_position = [ori_x, new_y]
            elif y > 0 and not cell.bottom_wall.draw_to_screen:
                self.relative_grid_position = [ori_x, new_y]

    def _move_to_nxt_cell_position(self):
        # move the player to the new cell's center position
        cell = self._get_cell_from_grid()
        self.rect.center = cell.rect.center

    def collide_target(self):
        """assume target is not None => kill the target existence from the screen"""
        if pygame.sprite.collide_rect(self, self.target):
            self.target.kill()

    def update(self):
        """update the position of the player and target collsion logics"""
        self._move_to_nxt_cell_position()

        self.collide_target()


class Destination(pygame.sprite.Sprite):
    """object that the player need to collide with"""

    size = WALL_LENGTH - (WALL_LENGTH * 0.2)

    def __init__(self, center_x, center_y):
        super().__init__()

        self.image = pygame.Surface([self.size, self.size])
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        # place at this cooridinate
        self.rect.center = (center_x, center_y)