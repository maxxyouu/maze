"""
use a path finding algorithm to imitate a AI that find the path to the destination
"""

class PathFinder:
    """use BFS or DFS algorithm to find the path from begining to end"""

    def __init__(self, start_cord, end_cord, tree_map):
        """
        @type start_cord: tuple
        @type end_cord: tuple
        @type tree_map: 2-d list
        """
        self.start_cord = start_cord
        self.end_cord = end_cord
        # only modify the copy of the 2d list
        self.tree_map = tree_map

        # reset all cell properties
        self._reset_cellProperties()

        self.start_cell = self.tree_map[self.start_cord[0]][self.start_cord[1]]
        self.end_cell = self.tree_map[self.end_cord[0]][self.end_cord[1]]

        # generate a tree map relationship btw cells by changing the adjacent_cells list of each cell
        self.treeConstructor = TreeConstructor(self.tree_map)
        self.treeConstructor.generate_tree(self.start_cell)

    def _reset_cellProperties(self):
        # reset al lthe cell tree properties
        for column in self.tree_map:
            for cell in column:
                cell.reset_treeProperties()

    def recursive_depth_first_search(self, x, y):
        """find the path from self.start_cell to self.end_cell
        note: this method only works for small maze map
        @return None
            modify self.id_path
        """
        cell = self.tree_map[x][y]  # get the cell
        if cell.id == self.end_cell.id:
            return [cell.id]
        elif cell.adjacent_cells:
            for adjacent_cell in cell.adjacent_cells:
                x, y = adjacent_cell.id
                path = self.recursive_depth_first_search(x, y)
                if path:
                    return [cell.id] + path
        else:
            return []
    
    def depth_first_search(self, x, y):
        """implement depth-first search algorithm by using loop only
        this function can generate the path for any maze map
        """
        stack = [self.tree_map[x][y]]
        path = []
        while stack:
            cell = stack.pop(0)
            path.append(cell.id)
            if cell.id == self.end_cell.id:
                return path
            elif not cell.adjacent_cells:
                path.pop()
            else:
                for adjacent_cell in cell.adjacent_cells:
                    x, y = adjacent_cell.id
                    stack.append(self.tree_map[x][y])
        return path


class TreeConstructor:
    """create a tree structure based on the grid system in the maze
    use the grid system after the GameController.initialize_map()
    """
    def __init__(self, maze_grid):
        """
        @type maze_grid: 2-D grid system after GameController.initialize_map()
        """
        self.maze_grid = maze_grid

    def generate_tree(self, initial_cell):
        """
        call construct_Cell_relations() then use this method
        clean up the relationship graph in to a tree map starts at position (0,0)
        in grid coordinate system
        """
        def construct_cell_relations():
            """
            create relationship btw Cell objs by modify the cell.adjacent_cells list
            the final graph structure has MULTIPLE cycle conditions, handle it in the next method
            @return None
            """
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
                            if neighbour == 'top' and not current_cell.top_wall.draw:
                                current_cell.adjacent_cells.append(self.maze_grid[x][y - 1])
                            elif neighbour == 'right' and not current_cell.right_wall.draw:
                                current_cell.adjacent_cells.append(self.maze_grid[x + 1][y])
                            elif neighbour == 'bottom' and not current_cell.bottom_wall.draw:
                                current_cell.adjacent_cells.append(self.maze_grid[x][y + 1])
                            elif neighbour == 'left' and not current_cell.left_wall.draw:
                                current_cell.adjacent_cells.append(self.maze_grid[x - 1][y])
        
        def clean_relations(starting_cell):
            """
            clean up all the cycle conditions in the graph system
            make sure no looping conditions by futher modify the adjacent_list for each cell
            call this after (1)
            use cell.tree_visited condition to determine the cycle condition and modify the adjacent list

            @type starting_cell: cell obj
            @return None
            """
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

        # call the helper functions
        construct_cell_relations()
        # get the root of the graph
        clean_relations(initial_cell)