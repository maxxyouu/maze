"""construct a tree structure for the cell objects by modify cell's attributes"""

class TreeConstructor:
    """
    create a tree structure based on the grid system in the maze
    use the grid system after the GameController.initialize_map()
    """

    def __init__(self, maze_grid):
        """
        @type maze_grid: 2-D grid system after GameController.initialize_map()
        """
        self.maze_grid = maze_grid

    def _construct_cell_relations(self):
        # create relationship btw Cell objs by modify the cell.adjacent_cells list
        # the final graph structure has MULTIPLE cycle conditions, handle it in the next method
        # @return None

        # for each col in the grid
        for x in range(len(self.maze_grid)):
            # for each cell in that col
            for y in range(len(self.maze_grid[x])):

                current_cell = self.maze_grid[x][y]
                neighbours = current_cell.neighbour_cells  # a dictionary

                for neighbour in neighbours:
                    # check neighbour if not None
                    if neighbours[neighbour]:
                        # check each wall condition
                        # append nxtcell to the this.adjacent_cell list
                        if neighbour == 'top' and not current_cell.top_wall.draw_to_screen:
                            current_cell.adjacent_cells.append(self.maze_grid[x][y - 1])
                        elif neighbour == 'right' and not current_cell.right_wall.draw_to_screen:
                            current_cell.adjacent_cells.append(self.maze_grid[x + 1][y])
                        elif neighbour == 'bottom' and not current_cell.bottom_wall.draw_to_screen:
                            current_cell.adjacent_cells.append(self.maze_grid[x][y + 1])
                        elif neighbour == 'left' and not current_cell.left_wall.draw_to_screen:
                            current_cell.adjacent_cells.append(self.maze_grid[x - 1][y])

    def _clean_relations(self, starting_cell):
        # clean up all the cycle conditions in the graph system
        # make sure no looping conditions by futher modify the adjacent_list for each cell
        # call this after (1)
        # use cell.tree_visited condition to determine the cycle condition and modify the adjacent list
        #
        # @type starting_cell: cell obj
        # @return None

        queue = [starting_cell]
        while queue != []:
            # pop the first cell in the queue
            cell = queue.pop(0)
            # mark the current cell is visited in the tree structure
            cell.tree_visited = True
            # eliminate the cycle structure
            cell.adjacent_cells = [adjacent_cell for adjacent_cell in cell.adjacent_cells
                                                 if not adjacent_cell.tree_visited]
            # append the tree structure to the queue
            queue += cell.adjacent_cells

    def generate_tree(self, initial_cell):
        """
        call construct_Cell_relations() then use this method
        clean up the relationship graph in to a tree map starts at position (0,0)
        in grid coordinate system
        """
        # call the helper functions
        self._construct_cell_relations()
        # get the root of the graph
        self._clean_relations(initial_cell)