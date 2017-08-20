"""helper functions that ease the game"""

def normalize_screen_size(width, height, divisiable_num):
    """
    return a new width and height value that is divisible by the relative_size
    :param width: int
    :param height: int
    :param divisiable_num: int
    :return: tuple of different width and height
    """
    new_width = width - width % divisiable_num
    new_height = height - height % divisiable_num
    return new_width, new_height