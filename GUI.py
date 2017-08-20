"""GUI object that handle all the gui display"""
import pygame
from Constants import SCREEN_LENGTH, SCREEN_WIDTH

# REFERENCE:https://github.com/20021307/Pygame/blob/master/reaction_game/main.py


class GuiManager:
    """all the gui components are here"""

    def __init__(self, screen):
        """
        :param screen: pygame screen surface
        """
        self.screen = screen

    def set_msg_as(self, font_name, msg, color, size, bold=False, italic=False):
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

    def generate_btn(self, width, height, bg_color, center_pos_x, center_pos_y):
        """ generate a button onto the screen
        :param width: int
        :param height: int
        :param bg_color: RGB
        :param center_pos_x: int
        :param center_pos_y: omt
        :return:
        """
        pass

    def intro_screen(self):
        """
        create introduction for the game at the beginning
        :return:
        """
        pass

    def instruction(self):
        """
        instruction screen for player to read
        :return:
        """
        pass

    def ending_screen(self):
        """
        display this when the game has ended
        :return:
        """
        pass

    def display_statistics(self, level_statistics):
        """
        display each level's time from level_statistics
        :param level_statistics: dictionary
        :return: None
        """
        pass

    def show_msg_to_screen(self):
        """
        blit msg to the screen
        :return: None
        """
        pass

