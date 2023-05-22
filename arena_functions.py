"""
Funciones utilizadas por la clase Arena para obtener datos del juego
"""

from difflib import SequenceMatcher
import threading
from PIL import ImageGrab
import numpy as np
import requests
import screen_coords
from ocr import get_text_from_image, ROUND_WHITELIST, ALPHABET_WHITELIST
import game_assets
import bot_functions
from vec4 import Vec4
import screen_coords
import settings
import pydirectinput

def get_round(image: ImageGrab.Image) -> str:
    """Gets the current game round"""
    n_round = image.crop(screen_coords.ROUND_POS.get_coords())
    game_round = get_text_from_image(image=n_round)
    return game_round

def get_level_image(image: ImageGrab.Image):
    return image.crop(screen_coords.LEVEL_POS.get_coords())

def get_level(image: ImageGrab.Image) -> int:
    level = get_level_image(image)
    return get_text_from_image(level, whitelist=ROUND_WHITELIST)

def get_healths(image):
    healths = {}
    for POS in screen_coords.PLAYERS_HEALTH_POS:
        player_image = image.crop(POS.get_coords())
        player_name = player_image.crop(screen_coords.PLAYER_NAME_POS.get_coords())
        player_name = get_text_from_image(player_name, whitelist=ALPHABET_WHITELIST+ROUND_WHITELIST)
        player_heath = player_image.crop(screen_coords.PLAYER_HEALTH_POS.get_coords())
        player_heath = get_text_from_image(player_heath, whitelist=ROUND_WHITELIST)
        healths[player_name] = player_heath
    return healths

def get_own_health(image: ImageGrab.Image) -> int:
    player_health = 1
    for POS in screen_coords.PLAYERS_HEALTH_POS:
        player = image.crop(POS.get_coords())
        player_name = player.crop(screen_coords.PLAYER_NAME_POS.get_coords())
        player_name = get_text_from_image(player_name, whitelist=ALPHABET_WHITELIST+ROUND_WHITELIST)
        if player_name == settings.USERNAME:
            player_health = player.crop(screen_coords.PLAYER_HEALTH_POS.get_coords())
            player_health = get_text_from_image(player_health, whitelist=ROUND_WHITELIST)
            break
    return player_health

def get_gold(image: ImageGrab.Image) -> int:
    gold_image = image.crop(screen_coords.GOLD_POS.get_coords())
    gold = get_text_from_image(gold_image)
    return gold


def valid_champ(champ: str) -> str:
    """Hace coincidir la cadena de campeón con una cadena de nombre de campeón válida y la devuelve"""
    if champ in game_assets.CHAMPIONS:
        return champ

    return next(
        (
            champion
            for champion in game_assets.CHAMPIONS
            if SequenceMatcher(a=champion, b=champ).ratio() >= 0.7
        ),
        "",
    )

def get_shop(image: ImageGrab.Image) -> list:
    """Devuelve la lista de campeones en la tienda."""
    shop = []
    champ_names_image = image.crop(screen_coords.CHAMP_NAME_POS.get_coords())
    for index, POS in enumerate(screen_coords.CHAMPIONS_NAME_POS):
        cut = champ_names_image.crop(POS.get_coords())
        champ_name = get_text_from_image(cut)
        champ_name = ''.join(e for e in champ_name if e.isalnum() or e == ' ').strip()
        shop.append((index+1, valid_champ(champ_name)))
    return shop

def choose_item():
    bot_functions.left_click(screen_coords.ITEMS_POS[1].get_coords())

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

def buy_champion(i):
    pydirectinput.press(i)