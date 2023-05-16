"""
Contains static item & champion data
"""

import autochess

CHAMPIONS: dict[str, dict[str, int]] = {champion['name']: {"Gold": champion['cost'], "Board Size": 1} for champion in autochess.json['personajes']}

def champion_board_size(champion: str) -> int:
    """Toma una cadena (nombre del campeón) y devuelve el tamaño del tablero del campeón"""
    return CHAMPIONS[champion]["Board Size"]


def champion_gold_cost(champion: str) -> int:
    """Toma una cadena (nombre del campeón) y devuelve el oro del campeón"""
    return CHAMPIONS[champion]["Gold"]
