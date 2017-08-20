""" Generate a maze object using depth-first search backtracking algorithm """
import random
from Cell import *
from Utilities import normalize_screen_size
from Constants import SCREEN_WIDTH, SCREEN_LENGTH, WALL_LENGTH


class Maze:
    """actual maze objects"""

    def __init__(self, screen):
        """
        Construct a abstract 2-d array object to represent grid of walls and cells
        @type screen: screen object to display
        """
        # construct a abstract grid system list of list of cell objects
        # x --> x position in the screen; y --> y position in the screen
        self.grid = []

        self.unvisited_cell_dict = {}  # {str_id: bool}

        col = 0
        width, height = normalize_screen_size(SCREEN_WIDTH, SCREEN_LENGTH, WALL_LENGTH)
        for x in range(0, width, WALL_LENGTH):
            self.grid.append([])  # create a new col in the screen
            row = 0
            for y in range(0, height, WALL_LENGTH):
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
    
    def generate_maze(self, current_cell):
        """using loop to generate the maze by disable the walls in the cell
        @type current_cell: Cell
        """
        def _get_unvisited_neighbours(cur_cell):
            # get all the neighbour cells that are unvisited
            temp = cur_cell.neighbour_cells  # a temp dictionary of cells

            # the following check if the cell has the neighbour and not visited
            return [temp[n_cell] for n_cell in temp
                    if temp[n_cell] and not temp[n_cell].visited]
        
        def _remove_walls_btw(cur_cell, nxt_cell):
            # current and nxt are Cell obj
            # use the cell id to determine the relative position btw cell1 and cell2
            if cur_cell.id[0] == nxt_cell.id[0]:  # top of bottom

                if cur_cell.id[1] < nxt_cell.id[1]:  # top cells
                    cur_cell.bottom_wall.draw_to_screen = nxt_cell.top_wall.draw_to_screen = False
                elif cur_cell.id[1] > nxt_cell.id[1]:
                    cur_cell.top_wall.draw_to_screen = nxt_cell.bottom_wall.draw_to_screen = False
            
            elif cur_cell.id[1] == nxt_cell.id[1]:  # left or right

                if cur_cell.id[0] < nxt_cell.id[0]:
                    cur_cell.right_wall.draw_to_screen = nxt_cell.left_wall.draw_to_screen = False
                elif cur_cell.id[0] > nxt_cell.id[0]:
                    cur_cell.left_wall.draw_to_screen = nxt_cell.right_wall.draw_to_screen = False

        # main logic of create the maze
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
                

