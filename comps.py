COMP = {
    "Redaxe Chief": {
        "board_position": 5,
        "items": ["InfinityEdge", "LastWhisper", "GiantSlayer"],
        "level": 3,
        "final_comp": True,
    },
    "Tusk Champion": {
        "board_position": 6,
        "items": ["JeweledGauntlet", "StatikkShiv", "HextechGunblade"],
        "level": 3,
        "final_comp": False
    },
    "Unicorn": {
        "board_position": 13,
        "items": [],
        "level": 3,
        "final_comp": True
    },
    "Frost Knight": {
        "board_position": 22,
        "items": [],
        "level": 3,
        "final_comp": True,
    },
    "Resentful Murk": {
        "board_position": 23,
        "items": ["Bloodthirster", "TitansResolve"],
        "level": 3,
        "final_comp": True,
    },
    "The Source": {
        "board_position": 24,
        "items": ["LocketoftheIronSolari", "LocketoftheIronSolari", "IonicSpark"],
        "level": 3,
        "final_comp": True,
    },
    "Sky Breaker": {
        "board_position": 25,
        "items": [],
        "level": 3,
        "final_comp": True
    },
    "Shining Archer": {
        "board_position": 25,
        "items": [],
        "level": 3,
        "final_comp": True
    },
    "Ogre Mage": {
        "board_position": 26,
        "items": [],
        "level": 3,
        "final_comp": True,
    }
}

def champions_to_buy() -> list:
    para_comprar: list = []
    for champion, champion_data in COMP.items():
        if champion_data["level"] == 1:
            para_comprar.append(champion)
        elif champion_data["level"] == 2:
            para_comprar.extend([champion] * 3)
        elif champion_data["level"] == 3:
            para_comprar.extend([champion] * 9)
        else:
            raise ValueError("Comps.py | El level debe de ser (1-3)")
    return para_comprar


def get_unknown_slots() -> list:
    container: list = []
    for _, champion_data in COMP.items():
        container.append(champion_data["board_position"])
    return [n for n in range(27) if n not in container]
