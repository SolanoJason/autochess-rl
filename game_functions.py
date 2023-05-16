"""
Functions used by the Game class to retrieve relevant data
"""

from time import sleep
from PIL import ImageGrab
import screen_coords
import ocr
import game_assets
import bot_functions


def get_round() -> str:
    """Gets the current game round"""
    screen_capture = ImageGrab.grab(bbox=screen_coords.ROUND_POS.get_coords())
    n_round = screen_capture.crop(screen_coords.ROUND_POS.get_coords())
    game_round = ocr.get_text_from_image(image=n_round)
    return game_round