"""
Contiene toda la información relacionada con una ranura de tablero individual utilizada por el bot
"""
from collections import Counter
from utils import *


class LineUp:
    def __init__(self, lineup):
        self.lineup = lineup

    def get_champions(self):
        return [(champion.name, champion.level) for champion in self.lineup]

    def count_same_champion(self, champion):
        counts = Counter(self.get_champions())
        return counts[(champion.name), champion.level]

    def can_upgrade(self, new_champion):
        if self.count_same_champion(new_champion) == 1:
            return True

    def add_champion(self, new_champion):
        if self.can_upgrade(new_champion):
            indices_list = []
            for i, champion in enumerate(self.lineup):
                if champion.name == new_champion.name and champion.level == new_champion.level:
                    indices_list.append(i)
            delete_multiple_element(self.lineup, indices_list)
            new_champion.level += 1
        self.lineup.append(new_champion)

    def remove_champion(self, old_champion):
        self.lineup.remove(old_champion)

    def get_value(self, level):
        main_lineup = sorted(self.lineup, key=lambda c:c.value, reverse=True)[:level]
        bench = sorted(self.lineup, key=lambda c:c.value, reverse=True)[level:]
        main_lineup_value = sum(map(lambda c: c.value, main_lineup))
        bench_value = sum(map(lambda c: c.value, bench))
        return main_lineup_value + bench_value / 3

    def __str__(self) -> str:
        return str(self.lineup)

    def __repr__(self) -> str:
        return self.__str__()


class Champion:
    """Clase de campeón que contiene información sobre una sola unidad en el tablero o banco"""

    def __init__(self, name, level, pv, atk, atk_speed, armor, magic_resistance, atk_range, player_damage, cost, race, classes) -> None:
        self.name = name
        self.level = level
        self.pv = pv
        self.atk = atk
        self.atk_speed = atk_speed
        self.armor = armor
        self.magic_resistance = magic_resistance
        self.atk_range = atk_range
        self.player_damage = player_damage
        self.cost = cost
        self.race = race
        self.classes = classes
        self.value = (self.pv / 100 + self.atk / 10 + (3-self.atk_speed)*10 + self.armor*2 +
                      self.magic_resistance/2 + self.atk_range/2 + self.player_damage + self.cost*3) * (self.level + 1)

    def does_need_items(self):
        """Devuelve si la instancia de campeón necesita elementos"""
        return len(self.completed_items) != 3 or len(self.build) + len(self.current_building) == 0

    def __str__(self) -> str:
        return f'{self.name} {self.level} {self.value=}'

    def __repr__(self) -> str:
        return self.__str__()
