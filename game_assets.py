"""
Contains static item & champion data
"""

import autochess
from Entitys import *

CHAMPIONS: dict[str, dict[str, int]] = {champion['name']: Champion(**champion, level=1) for champion in autochess.json['personajes']}
PVE_ROUND: set[str] = {"1", "2", "3", "10", "15", "20", "25", "30", "35", "40", "45", "50"}

def champion_board_size(champion: str) -> int:
    """Toma una cadena (nombre del campeón) y devuelve el tamaño del tablero del campeón"""
    return CHAMPIONS[champion]["Board Size"]


def champion_gold_cost(champion: str) -> int:
    """Toma una cadena (nombre del campeón) y devuelve el oro del campeón"""
    return CHAMPIONS[champion]["Gold"]

