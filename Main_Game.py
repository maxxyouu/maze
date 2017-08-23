"""To start of the game => RUN THIS"""
import pygame
from GameController import GameController
from Constants import *
from Utilities import *

INSTRUCTIONS_WAIT_TIME = 2000


def show_instructions(screen):
    """
    show instruction to the screen of how to player the games
    :param screen: pygame surface
    :return: None
    """
    msg1 = 'Press A to find the path to the target'
    msg2 = 'Press D to enable movements'
    msg3 = 'Use arrow keys to move the player'
    msg1_surface, msg1_rect = set_msg_as(GAME_FONT, msg1, LIGHTGRAY, 20, True)
    msg2_surface, msg2_rect = set_msg_as(GAME_FONT, msg2, LIGHTGRAY, 20, True)
    msg3_surface, msg3_rect = set_msg_as(GAME_FONT, msg3, LIGHTGRAY, 20, True)
    vertical_pos = SCREEN_LENGTH // 3
    msg1_position = (SCREEN_WIDTH // 2, vertical_pos)
    msg2_position = (SCREEN_WIDTH // 2, 1.5 * vertical_pos)
    msg3_position = (SCREEN_WIDTH // 2, 2 * vertical_pos)
    show_msg_to_screen(msg1_surface, msg1_rect, msg1_position, screen)
    show_msg_to_screen(msg2_surface, msg2_rect, msg2_position, screen)
    show_msg_to_screen(msg3_surface, msg3_rect, msg3_position, screen)


def main():
    """main function to handle the game"""

    pygame.init()
    width, height = normalize_screen_size(SCREEN_WIDTH, SCREEN_LENGTH, WALL_LENGTH)
    screen = pygame.display.set_mode([width, height])
    game_controller = GameController(screen)
    pygame.display.set_caption('Maze War')

    # show the instruction first before start play the game
    show_instructions(screen)
    pygame.time.wait(INSTRUCTIONS_WAIT_TIME)
    pygame.display.update()

    # display maze
    screen.fill(BLACK)
    game_controller.walls.draw(screen)
    game_controller.moving_sprites.draw(screen)
    pygame.display.update()

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
