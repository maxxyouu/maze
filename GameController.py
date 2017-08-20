"""main game"""
from Player import *
from Maze import *
from Constants import *
from PathFinder import *


class GameController:
    """main game controller to handle the logic"""

    def __init__(self, reference_screen, current_level=1, level_stat={}):
        """
        set up the game screen and all the setting of the game
        :param reference_screen: screen surface
        :param current_level: int current level number
        :param level_stat: dictionary of {level_bum: time in seconds}
        """

        # for game level logic
        self.targets_per_level_counter = 1
        self.current_level = current_level
        self.levels_stat = level_stat

        self.screen = reference_screen

        # sprite group
        self.wall_sprites = pygame.sprite.Group()
        self.moving_sprites_group = pygame.sprite.Group()

        # for path finding
        self.ai_path = pygame.sprite.Group()
        self.path_copy = self.ai_path.copy()

        self.maze = Maze(self.screen)
        self.maze_grid = self.maze.grid

        # default position for the player
        start_cell = self.maze.get_cell(0, 0)
        # this use algorithm to disable walls between cells
        self.maze.generate_maze(start_cell)

        # insert all the wall sprites to the group so that it can be drawn later
        self._build_wall_sprites(self.wall_sprites)

        # initialize default position
        self.target_x_index = -1
        self.target_y_index = -1
        self.player_x_index = 0
        self.player_y_index = 0

        # set destination obj to the random location in the maze
        self.target_x_index, self.target_y_index = self._select_indices_in_grid('Target')
        self.target = Target(self.target_x_index, self.target_y_index, self.maze_grid)
        # assign player position
        self.player_x_index, self.player_y_index = self._select_indices_in_grid('Player')
        self.player = Player(self.maze_grid, self.player_x_index, self.player_y_index, self.target)

        # add player and destination sprites
        self.moving_sprites_group.add(self.player, self.target)

        self.previous_ticked_time = pygame.time.get_ticks()

        self.show_path = False  # condition to show the path on the screen
        self.freeze_event_movements = False  # condition to move the player

    def _build_wall_sprites(self, sprite_group):
        # insert all the wall sprites from the .draw_to_screen variable to the group so that it can be drawn later
        # @type sprite_group: a sprite group

        for column in self.maze_grid:
            for cell in column:
                # conditions: if the wall should be drawn to the screen, then add to the sprite_group
                if cell.top_wall.draw_to_screen:
                    cell.top_wall.add(sprite_group)
                if cell.bottom_wall.draw_to_screen:
                    cell.bottom_wall.add(sprite_group)
                if cell.left_wall.draw_to_screen:
                    cell.left_wall.add(sprite_group)
                if cell.right_wall.draw_to_screen:
                    cell.right_wall.add(sprite_group)

    def _select_indices_in_grid(self, sprite='Player'):
        # create a random coordinate from the grid system
        # @return tuple
        def generate_two_random_values():
            # return Tuple
            x = random.randint(0, len(self.maze_grid) - 1)
            y = random.randint(0, len(self.maze_grid[x]) - 1)
            return x, y
        x, y = generate_two_random_values()
        if sprite == 'Player':
            while (x, y) == (self.target_x_index, self.target_y_index):
                x, y = generate_two_random_values()
        elif sprite == 'Target':
            while (x, y) == (self.player_x_index, self.player_y_index):
                x, y = generate_two_random_values()
        return x, y

    def event_handler(self):
        """handle movement events of the player and system events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.freeze_event_movements:
                            self.player.horizontal_movement_handler(-1)
                    elif event.key == pygame.K_RIGHT:
                        if not self.freeze_event_movements:
                            self.player.horizontal_movement_handler(1)
                    elif event.key == pygame.K_UP:
                        if not self.freeze_event_movements:
                            self.player.vertical_movement_handler(-1)
                    elif event.key == pygame.K_DOWN:
                        if not self.freeze_event_movements:
                            self.player.vertical_movement_handler(1)
                    elif event.key == pygame.K_a:  # the key for show the path
                        self._build_ai_path(self.player.relative_grid_position, [self.target_x_index,
                                                                                 self.target_y_index])
                        self.path_copy = self.ai_path.copy()

                        self.show_path = True
                        self.freeze_event_movements = True
                    elif event.key == pygame.K_d:
                        self.show_path = False
                        self.freeze_event_movements = False
                    elif event.key == pygame.K_ESCAPE:
                        # another way to close the game window
                        # another way to close the game window
                        self.show_statistics()
                        return True
        return False

    def _build_ai_path(self, start_coordinate, end_coordinate):
        # create the path from the start cell to the end cell

        # empty the path sprite group so the next path can override it
        self.ai_path.empty()

        # start to build the ai path toward the end_cells>
        path_finder = PathFinder(start_coordinate, end_coordinate, self.maze_grid)

        try:
            cells_coordinates = path_finder.depth_first_search_by_recursion(start_coordinate[0], start_coordinate[1])
            for x, y in cells_coordinates:
                # GET THE CELL AND FILL THE COLOR
                path_cell = self.maze_grid[x][y]
                path_cell.set_color(BLUE)
                self.ai_path.add(path_cell)

                # set the color for start and end position
                self.maze_grid[start_coordinate[0]][start_coordinate[1]].set_color(RED)  # start_cell color
                self.maze_grid[end_coordinate[0]][end_coordinate[1]].set_color(GREEN)  # end_cell color
        except RecursionError:
            print('You have pushed the AI algorithm to the limit, get closer to the target and try again')

    def _show_ai_path(self):
        # show the ai path onto the screen call in the draw_frame function
        if self.show_path:
            self.ai_path = self.path_copy
            self.ai_path.draw(self.screen)
        if not self.show_path:
            self.ai_path = pygame.sprite.Group()

    def draw_frame(self):
        """update the screen by updating all sprites and screen"""

        self.moving_sprites_group.update()

        # CLEAR THE PREVIOUS SPRITES
        self.screen.fill(BLACK)

        # UPDATE THE LATEST POSITION OF ALL SPRITES
        self.moving_sprites_group.draw(self.screen)
        self._show_ai_path()
        self.wall_sprites.draw(self.screen)
        pygame.display.update()

    def _reset_all(self):
        # reset all the sprite groups and and timer variables for a new maze get started
        self.moving_sprites_group.empty()
        self.wall_sprites.empty()
        self.moving_sprites_group = self.wall_sprites = self.player = self.target = self.maze = self.previous_ticked_time = None

    def replay(self, screen):
        """once the destination are not in the screen, redraw the map"""

        if len(self.moving_sprites_group) <= 1:
            # get the delta time that finished the game
            if self.targets_per_level_counter < TARGETS_PER_LEVEL:
                self._locate_target_at_level()
                self.targets_per_level_counter += 1
            else:
                delta_time_in_seconds = str((pygame.time.get_ticks() - self.previous_ticked_time) / 1000)
                # store the statistics to
                self.levels_stat[self.current_level] = delta_time_in_seconds + 's'

                # clear all sprite:
                self._reset_all()
                # redraw the maze map, player, and destination
                self.__init__(screen, self.current_level + 1, self.levels_stat)

    def _locate_target_at_level(self):
        """relocate the target in the same map when meet the condition"""

        if len(self.moving_sprites_group) <= 1:
            # in case it relocate to the same location
            self.target_x_index, self.target_y_index = self._select_indices_in_grid()
            self.target = Target(self.target_x_index, self.target_y_index)

            # set target
            self.player.target = self.target
            # add the target to the sprite group
            self.moving_sprites_group.add(self.target)

            # rethink the ai_path
            self._build_ai_path(end_coordinate=[self.target_x_index, self.target_y_index])
            self.path_copy = self.ai_path.copy()

    def show_statistics(self):
        """
        display in the console about the time finsihed for each level
        :return: None
        """
        for level in self.levels_stat:
            print('level{} is finished'.format(level))
            print('Time finished for this level in seconds: {}s'.format(str(self.levels_stat[level])))
