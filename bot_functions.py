"""
Handles sending input to the game, coords contain a cartesian ordered pair (x, y)
"""

import random
import pydirectinput
from screen_coords import *


def left_click(coords: tuple) -> None:
    offset: int = random.randint(-3, 3)
    pydirectinput.moveTo(coords[0] - offset, coords[1] - offset)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()


def right_click(coords: tuple) -> None:
    offset: int = random.randint(-3, 3)
    pydirectinput.moveTo(coords[0] - offset, coords[1] - offset)
    pydirectinput.mouseDown(button="right")
    pydirectinput.mouseUp(button="right")


def press_e(coords: tuple) -> None:
    offset: int = random.randint(-3, 3)
    pydirectinput.moveTo(coords[0] - offset, coords[1] - offset)
    pydirectinput.press("e")


def move_mouse(coords: tuple) -> None:
    pydirectinput.moveTo(coords[0], coords[1])
 

def buy_xp() -> None:
    pydirectinput.press("f")

def toggle_shop():
    pydirectinput.press("space")

def toggle_items():
    pydirectinput.press("v")

def toggle_lineup():
    pydirectinput.press("tab")

def distribute_items():
    pydirectinput.press("c")

def distribute_pieces():
    pydirectinput.press("q")

def reroll() -> None:
    pydirectinput.press("d")

def press_esc() -> None:
    pydirectinput.press("esc")

def choose_item():
    left_click(ITEMS_POS[1].get_coords())

