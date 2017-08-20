""" use a path finding algorithm to imitate a AI that find the path to the destination """
from Tree_Constructor import TreeConstructor


class PathFinder:
    """use BFS or DFS algorithm to find the path from beginning to end"""

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

        # reset all cell properties before generate the tree map each time create self object
        self._reset_cell_properties()

        self.start_cell = self.tree_map[self.start_cord[0]][self.start_cord[1]]
        self.end_cell = self.tree_map[self.end_cord[0]][self.end_cord[1]]

        # generate a tree map relationship btw cells by changing the adjacent_cells list of each cell
        self.treeConstructor = TreeConstructor(self.tree_map)
        self.treeConstructor.generate_tree(self.start_cell)

    def _reset_cell_properties(self):
        # reset all the cell tree properties
        for column in self.tree_map:
            for cell in column:
                cell.reset_treeProperties()

    def depth_first_search_by_recursion(self, x, y):
        """
        find the path from self.start_cell to self.end_cell
        note: this method only works restricted size maze map
        @return None modify self.id_path
        """
        cell = self.tree_map[x][y]  # get the cell
        if cell.id == self.end_cell.id:
            return [cell.id]
        elif cell.adjacent_cells:
            for adjacent_cell in cell.adjacent_cells:
                x, y = adjacent_cell.id
                path = self.depth_first_search_by_recursion(x, y)
                if path:
                    return [cell.id] + path
        else:
            return []
    
    def depth_first_search_by_loop(self, x, y):
        """
        implement depth-first search algorithm by using loop only
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


