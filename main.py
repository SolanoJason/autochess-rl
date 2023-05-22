"""
Donde comienza la ejecución del bot y contiene el ciclo del juego que mantiene el bot funcionando indefinidamente
"""

import multiprocessing
from game import Game
import settings
import screen_coords
from bot_functions import move_mouse, left_click, right_click
from PIL import ImageGrab, Image
from time import sleep
import pyautogui

def game_loop() -> None:
    """Mantiene el programa ejecutándose indefinidamente llamando a la cola y al inicio del juego en un bucle"""

    logo = Image.open('Photos/logo.png')
    box = pyautogui.locateOnScreen(logo, confidence=0.6)
    vec2 = pyautogui.center(box)
    pyautogui.click(vec2)
    sleep(3)

    left_click(screen_coords.HOME.get_coords())
    sleep(1)
    left_click(screen_coords.CUSTOM.get_coords())
    sleep(1)
    left_click(screen_coords.CREATE1.get_coords())
    sleep(1)
    left_click(screen_coords.CREATE2.get_coords())
    sleep(1)
    for _ in range(7):
        left_click(screen_coords.ADD_BOT.get_coords())
        sleep(0.5)
    left_click(screen_coords.START.get_coords())

    while True:
        Game()


if __name__ == "__main__":
    game_loop()
