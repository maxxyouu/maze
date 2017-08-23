"""main game"""
from Player import *
from Maze import *
from Constants import *
from PathFinder import *
from Utilities import *


class GameController:
    """main game controller to handle the logic"""

    def __init__(self, normalized_screen, current_level=1, level_stat={}):
        """
        set up the game screen and all the setting of the game
        :param normalized_screen: screen surface that is normalized
        :param current_level: int current level number
        :param level_stat: dictionary of {level_bum: time in seconds}
        """
        # for game level logic
        self.targets_per_level_counter = 1
        self.current_level = current_level
        self.levels_stat = level_stat
        self.restricted_path_used = PATH_USED_LIMIT
        self.popup_msg_counter = 1

        self.screen = normalized_screen

        # sprite group
        self.walls = pygame.sprite.Group()
        self.moving_sprites = pygame.sprite.Group()

        # for path finding
        self.ai_path = pygame.sprite.Group()
        self.path_copy = self.ai_path.copy()

        self.width, self.height = self.screen.get_size()
        self.maze = Maze(self.screen, self.width, self.height)
        self.maze_grid = self.maze.grid

        # default position for the player
        start_cell = self.maze.get_cell(0, 0)
        # this use algorithm to disable walls between cells
        self.maze.generate_maze(start_cell)
        # insert all the wall sprites to the group so that it can be drawn later
        self._build_wall_sprites(self.walls)

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
        self.moving_sprites.add(self.player, self.target)

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
            x_index = random.randint(0, len(self.maze_grid) - 1)
            y_index = random.randint(0, len(self.maze_grid[x_index]) - 1)
            return x_index, y_index

        x, y = generate_two_random_values()
        if sprite == 'Player':
            while (x, y) == (self.target_x_index, self.target_y_index):
                x, y = generate_two_random_values()
        elif sprite == 'Target':
            while (x, y) == (self.player_x_index, self.player_y_index):
                x, y = generate_two_random_values()
        return x, y

    def event_handler(self):
        """handle all the events of the game"""
        result = False
        for event in pygame.event.get():
            result = self._quit_events(event)
            if event.type == pygame.KEYDOWN:
                self._move_events(event)
                self._ai_events(event)
        return result

    def _quit_events(self, event):
        """
        quit the pygame
        :param event: event obj
        :return: bool
        """
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.show_statistics()
            pygame.time.wait(ENDING_WAIT_TIME)
            return True

    def _move_events(self, event):
        """
        handle movement for the player
        :param event: event obj with KEYDOWN
        :return: None
        """
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

    def _ai_events(self, event):
        """
        handle other game event in pygame
        :param event: event obj with KEYDOWN
        :return: None
        """
        if event.key == pygame.K_a:  # the key for show the path
            self._handle_ai()
        elif event.key == pygame.K_d:
            self.show_path = False
            self.freeze_event_movements = False

    def _handle_ai(self):
        """
        handle the AI event logic
        :return:
        """
        self.freeze_event_movements = True
        if self.restricted_path_used != 0:
            self.show_path = True
            self._build_ai_path(self.player.grid_position, self.target.grid_position)
            self.path_copy = self.ai_path.copy()
            self.restricted_path_used -= 1
        else:
            # print a message on the screen for a couple seconds
            self.popup_msg_counter += 1
            self._show_ai_msg()

    def _show_ai_msg(self):
        """
        assump the limit is passed, then called this method to show the message
        :return: None
        """
        main_msg = 'You have pass the path use limit, finish the game on your own'
        instruction_msg = 'Press D to enable the movement after the text is disappeared'
        main_msg_position = (self.width // 2, self.height // 3)
        instruction_msg_position = (self.width // 2, self.height // 2)
        main_message_surface, main_message_rect = set_msg_as(GAME_FONT, main_msg, WHITE, MAIN_FONT_SIZE, True)
        instruction_msg_surface, instruction_msg_rect = set_msg_as(GAME_FONT, instruction_msg, WHITE, SUB_FONT_SIZE,
                                                                   True)
        show_msg_to_screen(main_message_surface, main_message_rect, main_msg_position, self.screen)
        show_msg_to_screen(instruction_msg_surface, instruction_msg_rect, instruction_msg_position, self.screen)
        pygame.time.wait(MASSAGE_WAIT_TIME)

    def _build_ai_path(self, start_coordinate, end_coordinate):
        """
        :param start_coordinate: tuple
        :param end_coordinate: tuple
        :return: None
        """
        # empty the path sprite group so the next path can override it
        self.ai_path.empty()
        # start to build the ai path toward the end_cells>
        path_finder = PathFinder(start_coordinate, end_coordinate, self.maze_grid)
        try:
            player_x_index, player_y_index = start_coordinate
            target_x_index, target_y_index = end_coordinate
            cells_coordinates = path_finder.depth_first_search_by_recursion(player_x_index, player_y_index)
            # color the path
            self._color_ai_path(BLUE,
                                cells_coordinates,
                                player_x_index,
                                player_y_index,
                                target_x_index,
                                target_y_index)
        except RecursionError:
            # when the maze is too big for the recursion to proceed
            print('You have pushed the AI algorithm to the limit, get closer to the target and try again')

    def _color_ai_path(self, color, cells, start_x, start_y, end_x, end_y):
        """
        :param color: RBG color
        :param cells: list of coordinates
        :param start_x: x index of start position
        :param start_y: y index of start position
        :param end_x: x index of end position
        :param end_y: y index of end position
        :return: None
        """
        for x, y in cells:
            # GET THE CELL AND FILL THE COLOR
            path_cell = self.maze_grid[x][y]
            path_cell.set_color(color)
            self.ai_path.add(path_cell)
            # set the color for start and end position
            self.maze_grid[start_x][start_y].set_color(RED)
            self.maze_grid[end_x][end_y].set_color(GREEN)

    def _show_ai_path(self):
        # show the ai path onto the screen call in the draw_frame function
        if self.show_path:
            self.ai_path = self.path_copy
            self.ai_path.draw(self.screen)
        if not self.show_path:
            self.ai_path = pygame.sprite.Group()

    def _reset_all(self):
        # reset all the sprite groups and and timer variables for a new maze get started
        self.moving_sprites.empty()
        self.walls.empty()
        self.moving_sprites = self.walls = self.player = self.target = self.maze = self.previous_ticked_time = None

    def _locate_target_at_level(self):
        """relocate the target in the same map when meet the condition"""
        if len(self.moving_sprites) <= 1:
            # in case it relocate to the same location
            self.target_x_index, self.target_y_index = self._select_indices_in_grid()
            self.target = Target(self.target_x_index, self.target_y_index, self.maze_grid)
            # set target
            self.player.target = self.target
            # add the target to the sprite group
            self.moving_sprites.add(self.target)

    def _store_level_finished_time(self):
        # store the finished time in seconds into the self.level_stat
        delta_time = self._calculate_delta_time()
        # store the statistics to
        self.levels_stat[self.current_level] = delta_time

    def _calculate_delta_time(self):
        """
        calculate the time by subtracting the wait time from the pop up messages
        :return: str
        """
        delta_time = pygame.time.get_ticks() - self.previous_ticked_time
        delta_time -= self.popup_msg_counter * MASSAGE_WAIT_TIME
        delta_time = str(delta_time / 1000) + 's'
        return delta_time

    def show_statistics(self):
        """
        display in the console about the time finished for each level
        :return: None
        """
        for level in self.levels_stat:
            print('level-{} is finished'.format(level))
            print('Time finished for this level in seconds: {}'.format(str(self.levels_stat[level])))

    def replay(self, screen):
        """once the destination are not in the screen, redraw the map"""
        if len(self.moving_sprites) <= 1:
            if self.targets_per_level_counter < TARGETS_PER_LEVEL:
                self._locate_target_at_level()
                self.targets_per_level_counter += 1
            else:
                # get the delta time that finished the game
                self._store_level_finished_time()
                # clear all sprite:
                self._reset_all()
                # redraw the maze map, player, and destination
                self.__init__(screen, self.current_level + 1, self.levels_stat)

    def draw_frame(self):
        """update the screen by updating all sprites and screen"""

        self.moving_sprites.update()

        # CLEAR THE PREVIOUS SPRITES
        self.screen.fill(BLACK)

        # UPDATE THE LATEST POSITION OF ALL SPRITES
        self.moving_sprites.draw(self.screen)
        self._show_ai_path()
        self.walls.draw(self.screen)
        pygame.display.update()

    def _get_all_wall_rects(self, maze):
        """
        get all the wall's rectangles from the maze and store it in a list
        :param maze: 2-d list grid system
        :return: list of rectangles
        """
        rectangles = []
        for column in maze:
            for cell in column:
                if cell.top_wall.draw_to_screen:
                    rectangles.append(cell.top_wall)
                if cell.right_wall.draw_to_screen:
                    rectangles.append(cell.right_wall)
                if cell.bottom_wall.draw_to_screen:
                    rectangles.append(cell.bottom_wall)
                if cell.left_wall.draw_to_screen:
                    rectangles.append(cell.left_wall)
        return rectangles
