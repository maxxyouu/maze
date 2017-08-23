"""helper functions that ease the game
REFERENCE:https://github.com/20021307/Pygame/blob/master/reaction_game/main.py
"""
import pygame
from Constants import *


def normalize_screen_size(width, height, divisible_num):
    """
    return a new width and height value that is divisible by the relative_size
    :param width: int
    :param height: int
    :param divisible_num: int
    :return: tuple of different width and height
    """
    new_width = width - width % divisible_num
    new_height = height - height % divisible_num
    return new_width, new_height


def set_msg_as(font_name, msg, color, size, bold=False, italic=False):
    """ create a message txt with properties
    :param font_name: valid system font name as str
    :param msg: str
    :param color: rgb
    :param size: int font size
    :param bold: bool
    :param italic: bool
    :return: tuple (text_surface, rectangle)
    """
    text = pygame.font.SysFont(font_name, size, bold, italic)
    text_surface = text.render(msg, False, color)
    text_rectangle = text_surface.get_rect()
    return text_surface, text_rectangle


def show_msg_to_screen(msg_surface, msg_rect, msg_position, screen):
    """
    blit msg to the screen
    note: show be called after the set_msg_as() func
    :param msg_surface: str
    :param msg_rect: pygame.Rect
    :param msg_position: tuple
    :param screen: pygame.Surface
    :return: None
    """
    # set the center to the center position in the screen
    msg_rect.center = msg_position
    # show the msg to the screen
    screen.blit(msg_surface, msg_rect)
    pygame.display.update(msg_rect)

