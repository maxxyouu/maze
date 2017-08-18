"""
Generate a maze object using depth-first searth backtracking algorithm
"""
import pygame
import random

from Constants import *
from Cell import *

class Maze:
    """actual maze objects"""

    def __init__(self, screen):
        """Construct a abstrat 2-d array object to represent grid of walls and cells
        @type screen: screen object to display
        """
        # construc a abstract grid system list of list of cell objects
        # x --> x position in the screen; y --> y position in the screen
        self.grid = []
        # a unvisited dictionary {str_id: bool}
        self.unvisited_cell_dict = {}

        col = 0
        for x in range(0, SCREEN_WIDTH, WALL_LENGTH):
            self.grid.append([])  # create a new col in the screen
            row = 0
            for y in range(0, SCREEN_LENGTH, WALL_LENGTH):
                cell = Cell(x, y, screen)

                cell.set_id(col, row)
                self.unvisited_cell_dict[cell.str_id] = True

                self.grid[col].append(cell)
                row += 1
            col += 1

        def _assign_neighbours_to_cell(i, j):
            # handle all EDGE CASES
            # assign neighbours to grid[i][j]
            # x is the col_index
            # y is the row index
            # grid is self.grid
            # @return None
            cell = self.grid[i][j]
            # top neighbour
            if j - 1 >= 0:
                cell.neighbour_cells['top'] = self.grid[i][j - 1]
            # right neighbour
            if i + 1 < len(self.grid):
                cell.neighbour_cells['right'] = self.grid[i + 1][j]
            # bottom neighbour
            if j + 1 < len(self.grid[i]):
                cell.neighbour_cells['bottom'] = self.grid[i][j + 1]
            # left neighbour
            if i - 1 >= 0:
                cell.neighbour_cells['left'] = self.grid[i - 1][j]

        # assign neighbours to each cell object in the grid system
        for col_index in range(len(self.grid)):
            column = self.grid[col_index]
            for row_index in range(len(column)):
                _assign_neighbours_to_cell(col_index, row_index)
        
        # used for backtrack
        self.stack = []
        self.current_cell = None

    def get_cell(self, x, y):
        """get the cell at grid system coordinate x, y"""
        return self.grid[x][y]
    
    def large_maze_generator(self, current_cell):
        """using loop to generate the maze by disable the walls in the cell
        @type cell: Cell obj
        @type animate: a toggle to show the animation of the maze
        """
        def _get_unvisited_neighbours(current_cell):
            # get all the neighbour cells that are unvisited
            temp = current_cell.neighbour_cells  # a temp dictionary of cells

            # the following check if the cell has the neighbour and not visited
            return [temp[n_cell] for n_cell in temp
                                 if temp[n_cell] and not temp[n_cell].visited]
        
        def _remove_walls_btw(current, nxt):
            # current and nxt are Cell obj
            # use the cell id to determine the relative position btw cell1 and cell2
            if current.id[0] == nxt.id[0]:  # top of bottom
                if current.id[1] < nxt.id[1]:  # top cells
                    current.bottom_wall.draw = nxt.top_wall.draw = False
                elif current.id[1] > nxt.id[1]:
                    current.top_wall.draw = nxt.bottom_wall.draw = False
            elif current.id[1] == nxt.id[1]: # left or right
                if current.id[0] < nxt.id[0]:
                    current.right_wall.draw = nxt.left_wall.draw = False
                elif current.id[0] > nxt.id[0]:
                    current.left_wall.draw = nxt.right_wall.draw = False

        # main logics of create the maze
        while any(self.unvisited_cell_dict[cell] for cell in self.unvisited_cell_dict):

            current_cell.visited = True
            self.unvisited_cell_dict[current_cell.str_id] = False

            neighbours = _get_unvisited_neighbours(current_cell)
            if neighbours:
                # choose a random neighbour
                index = random.randint(0, len(neighbours) - 1)
                nxt_cell = neighbours[index]

                self.stack.append(nxt_cell)
                
                # disable the walls btw cells
                _remove_walls_btw(current_cell, nxt_cell)

                current_cell = nxt_cell
            elif self.stack:
                # set the popped cell to the current_cell
                current_cell = self.stack.pop()
                

