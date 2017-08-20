"""To start of the game => RUN THIS"""

import pygame
from GameController import GameController
from Constants import SCREEN_WIDTH, SCREEN_LENGTH, WALL_LENGTH, FRAME
from Utilities import normalize_screen_size


def main():
    """main function to handle the game"""
    pygame.init()
    width, height = normalize_screen_size(SCREEN_WIDTH, SCREEN_LENGTH, WALL_LENGTH)
    screen = pygame.display.set_mode([width, height])
    game_controller = GameController(screen)
    pygame.display.set_caption('Maze War')

    clock = pygame.time.Clock()
    done = False
    while not done:
        # handle all the event in the screen
        done = game_controller.event_handler()

        game_controller.draw_frame()

        game_controller.replay(screen)

        clock.tick(FRAME)

    pygame.quit()

if __name__ == '__main__':
    main()