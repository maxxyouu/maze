import pygame
from Player import *
from Maze import *
from Constants import *
from PathFinder import *

class GameController:
    """main game controller to handle the logic"""

    def __init__(self, reference_screen): 
        """set up the game screen and all the setting of the game"""
        # for game level logics
        self.counter = 0
       
        self.screen = reference_screen

        self.wall_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        # for path finding
        self.ai_path = pygame.sprite.Group()
        self.path_copy = self.ai_path.copy()

        self.maze = Maze(self.screen)
        self.maze_grid = self.maze.grid

        # default position for the player
        start_cell = self.maze.get_cell(0, 0)
        # this use algorithm to disable walls between cells
        self.maze.large_maze_generator(start_cell)

        # insert all the wall sprites to the group so that it can be drawn later
        for column in self.maze_grid:
            for cell in column:
                if cell.top_wall.draw:
                    cell.top_wall.add(self.wall_sprites)
                if cell.bottom_wall.draw:
                    cell.bottom_wall.add(self.wall_sprites)
                if cell.left_wall.draw:
                    cell.left_wall.add(self.wall_sprites)
                if cell.right_wall.draw:
                    cell.right_wall.add(self.wall_sprites)

        self.player = Player(self.maze_grid)

        # assign the wall sprite group obj to the player to interacts
        self.player.walls = self.wall_sprites
        
        # set destination obj to the random location in the maze
        self.endX_coordinate, self.endY_coordinate = self._select_coordinate()
        target_pos = self._generate_random_pos_for_destination(self.endX_coordinate, self.endY_coordinate)
        self.destination = Destination(target_pos[0], target_pos[1])
        self.counter += 1
        # set target
        self.player.target = self.destination

        # add player and destination sprites
        self.active_sprites.add(self.player, self.destination)

        # initialize the timer obj to time the delta to finish the game
        self.timer = pygame.time.get_ticks()

        self.show_path = False # condition to show the path on the screen
        self.freeze_event_movements = False # condition to move the player

    def _select_coordinate(self):
        # create a random coordinate from the grid system
        # @return tuple
        x = random.randint(0, len(self.maze_grid) - 1)
        y = random.randint(0, len(self.maze_grid[x]) - 1)
        return x, y

    def _generate_random_pos_for_destination(self, x, y):
        # """generate random position for the target """
        dest_cell = self.maze_grid[x][y]
        return dest_cell.rect.x, dest_cell.rect.y

    def event_handler(self):
        """handle movement events of the player and system events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.freeze_event_movements:
                            self.player.horizontal_movement_handler(-SPEED)
                    elif event.key == pygame.K_RIGHT:
                        if not self.freeze_event_movements:
                            self.player.horizontal_movement_handler(SPEED)
                    elif event.key == pygame.K_UP:
                        if not self.freeze_event_movements:
                            self.player.vertical_movement_handler(-SPEED)
                    elif event.key == pygame.K_DOWN:
                        if not self.freeze_event_movements:
                            self.player.vertical_movement_handler(SPEED)
                    elif event.key == pygame.K_a:  # the key for show the path

                        self._build_ai_path(self.player.relative_grid_position, [self.endX_coordinate,
                                                                                 self.endY_coordinate])
                        self.path_copy = self.ai_path.copy()
                    
                        self.show_path = True
                        self.freeze_event_movements = True
                    elif event.key == pygame.K_d:
                        self.show_path = False
                        self.freeze_event_movements = False
        return False

    def _build_ai_path(self, start_coordinate=[0, 0], end_coordinate=[-1, -1]):
        """create the path from the start cell to the end cell"""
        
        self.ai_path.empty()
        pathFinder = PathFinder(start_coordinate, end_coordinate, self.maze_grid)
        cells_coordinates = pathFinder.recursive_depth_first_search(start_coordinate[0], start_coordinate[1])
        # cells_coordinates = pathFinder.depth_first_search(start_coordinate[0], start_coordinate[1])

        for x, y in cells_coordinates:
            # GET THE CELL AND FILL THE COLOR
            path_cell = self.maze_grid[x][y]
            path_cell.set_color(BLUE)
            self.ai_path.add(path_cell)
        
        # set the color for start and end position
        start_cell = self.maze_grid[start_coordinate[0]][start_coordinate[1]]
        end_cell = self.maze_grid[end_coordinate[0]][end_coordinate[1]]
        start_cell.set_color(RED)
        end_cell.set_color(GREEN)
    
    def _show_ai_path(self):
        """show the ai path onto the screen call in the draw_frame function"""
        if self.show_path:
            self.ai_path = self.path_copy
            self.ai_path.draw(self.screen)
        if not self.show_path:
            self.ai_path = pygame.sprite.Group()

    def draw_frame(self):
        """update the screen by updating all sprites and screen"""
        
        self.active_sprites.update()

        # CLEAR THE PREIVOUS SPRITES
        self.screen.fill(BLACK)

        # UPDATE THE LATEST POSITION OF ALL SPRITES
        self.active_sprites.draw(self.screen)
        self._show_ai_path()
        self.wall_sprites.draw(self.screen)
        pygame.display.update()
    
    def _reset_all(self):
        self.active_sprites.empty()
        self.wall_sprites.empty()
        self.active_sprites = self.wall_sprites = self.player = self.destination = self.maze = self.timer = None

    def replay(self, screen):
        """once the destination are not in the screen, redraw the map"""

        if len(self.active_sprites) <= 1:
            # get the delta time that finished the game
            if self.counter < TARGETS_PER_MAZE:
                self._locate_target_at_level()
                self.counter += 1
            else:
                deltaTime = pygame.time.get_ticks() - self.timer
                print('level is finished')
                print('Time finished the maze in seconds: {}s'.format(str(deltaTime / 1000)))
                # clear all sprite:
                self._reset_all()
                # redraw the maze map, player, and destination
                self.__init__(screen)
    
    def _locate_target_at_level(self):
        """relocate the target in the same map when meet the condition"""
        
        if len(self.active_sprites) <= 1:
            x, y = self._select_coordinate()

            # in case it relocate to the same location
            while x == self.endX_coordinate and y == self.endY_coordinate:
                x, y = self._select_coordinate()
            self.endX_coordinate = x
            self.endY_coordinate = y
            target_pos = self._generate_random_pos_for_destination(self.endX_coordinate, self.endY_coordinate)
            self.destination = Destination(target_pos[0], target_pos[1])

            # set target
            self.player.target = self.destination
            # add the target to the sprite group
            self.active_sprites.add(self.destination)

            # rethink the ai_path
            self._build_ai_path(end_coordinate=(self.endX_coordinate, self.endY_coordinate))
            self.path_copy = self.ai_path.copy()

def main():
    """main function to handle the game"""
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_LENGTH])
    gameController = GameController(screen)
    pygame.display.set_caption('Maze')

    clock = pygame.time.Clock()
    done = False
    while not done:

        # handle all the event in the screen
        done = gameController.event_handler()

        gameController.draw_frame()

        gameController.replay(screen)

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()