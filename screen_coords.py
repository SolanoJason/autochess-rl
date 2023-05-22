"""
Contains static screen coordinates the bot uses
Screen coords for 1920x1080 screens
(x, y, x+w, y+h) for Vec4 locations, (x, y) for Vec2 locations
"""

from vec4 import Vec4, GameWindow
from vec2 import Vec2

PLAYERS_HEALTH_POS: list[Vec4] = [
    Vec4(GameWindow(0, 80, 280, 145)),
    Vec4(GameWindow(0, 145, 280, 210)),
    Vec4(GameWindow(0, 210, 280, 275)),
    Vec4(GameWindow(0, 275, 280, 340)),
    Vec4(GameWindow(0, 340, 280, 405)),
    Vec4(GameWindow(0, 405, 280, 470)),
    Vec4(GameWindow(0, 470, 280, 535)),
    Vec4(GameWindow(0, 535, 280, 600)),
]

PLAYER_NAME_POS = Vec4(GameWindow(110, 8, 200, 30))
PLAYER_HEALTH_POS = Vec4(GameWindow(172, 35, 215, 59))

# We have 8 pieces in auto chess
BENCH_HEALTH_POS: list[Vec4] = [
    Vec4(GameWindow(315, 771, 315+118, 771+108)),
    Vec4(GameWindow(440, 771, 440+118, 771+108)),
    Vec4(GameWindow(565, 771, 565+118, 771+108)),
    Vec4(GameWindow(685, 771, 685+112, 771+108)),
    Vec4(GameWindow(805, 771, 805+120, 771+108)),
    Vec4(GameWindow(930, 771, 930+115, 771+108)),
    Vec4(GameWindow(1050, 771, 1050+115, 771+108)),
    Vec4(GameWindow(1170, 771, 1170+115, 771+108)),
]

ROUND_POS: Vec4 = Vec4(GameWindow(185, 0, 250, 30))

CHAMP_NAME_POS = Vec4(GameWindow(240, 385, 1380, 415))

CHAMPIONS_NAME_POS = [
    Vec4(GameWindow(0, 0, 240, 35)),
    Vec4(GameWindow(240, 0, 450, 35)),
    Vec4(GameWindow(450, 0, 660, 35)),
    Vec4(GameWindow(660, 0, 870, 35)),
    Vec4(GameWindow(870, 0, 1080, 35)),
]

ITEMS_POS = [
    Vec4(GameWindow(320, 540, 440, 580)),
    Vec4(GameWindow(735, 540, 855, 580)),
    Vec4(GameWindow(1155, 540, 1275, 580)),
]

GOLD_POS: Vec4 = Vec4(GameWindow(1320, 10, 1368, 50))

LEVEL_POS: Vec4 = Vec4(GameWindow(178, 800, 220, 830))

HOME: Vec2 = Vec2(1360, 720)

CUSTOM: Vec2 = Vec2(1400, 865)

CREATE1: Vec2 = Vec2(980, 750)

CREATE2: Vec2 = Vec2(1047, 772)

ADD_BOT: Vec2 = Vec2(765, 225)

START: Vec2 = Vec2(1430, 837)