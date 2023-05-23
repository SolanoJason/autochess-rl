"""
Handles tasks that happen each game round
"""

from time import sleep, perf_counter
import random
import game_assets
from vec4 import Vec4
from vec2 import Vec2
from arena_functions import *
from PIL import Image, ImageGrab
from Entitys import *


class Game:
    """Clase de juego que maneja la lógica del juego, como tareas redondas."""

    def __init__(self) -> None:
        self.round = None
        self.lineup = LineUp(lineup=list())
        self.shop = []
        self.health = 100
        self.loading_screen()
        self.gold = 0
        # self.exp = 0
        self.level = 1

    def loading_screen(self) -> None:
        """Bucle que se ejecuta mientras el juego está en la pantalla de carga"""
        print("loading screen...")
        screenshot = ImageGrab.grab()
        round = get_round(screenshot)
        print(f'{round=}, {not round.isnumeric()}')
        while not round.isnumeric():
            print(f'{round=} hola {not round.isnumeric()}')
            screenshot = ImageGrab.grab()
            round = get_round(screenshot)
            sleep(0.4)
        self.game_loop()

    def get_new_shop_list(self):
        toggle_shop()
        sleep(0.4)
        reroll()
        sleep(0.4)
        screenshot = ImageGrab.grab()
        toggle_shop()
        print(f'{self.shop=}')
        sleep(0.4)
        return get_shop(screenshot)  

    def get_shop_list(self):
        toggle_shop()
        sleep(0.5)
        screenshot = ImageGrab.grab()
        toggle_shop()
        print(f'{self.shop=}')
        sleep(0.5)
        return get_shop(screenshot)

    def game_loop(self) -> None:
        """. 
        Bucle que se ejecuta mientras el juego está activo, 
        maneja la llamada a las tareas correctas para la ronda y la salida del juego."""
        print("game loop:")
        self.previous_round = None
        # while game_functions.check_alive():
        while True:
            screenshot = ImageGrab.grab()
            print(f'{get_round(screenshot)=}')
            if get_round(screenshot) != '':
                self.round: str = get_round(screenshot)
                if self.round != self.previous_round:
                    self.previous_round = self.round  
                    self.gold = get_gold(screenshot)
                    self.level = get_level(screenshot)
                    self.shop = self.get_shop_list()
                    self.health = get_own_health(screenshot)
                    self.do_round()
                sleep(0.5)

    def do_round(self):
        print(f"do round {self.round}----------------- \n")
        if str(int(self.round)-1) in game_assets.PVE_ROUND:
            toggle_items()
            sleep(0.5)
            choose_item()
            toggle_items()
        self.choose_action1(self.lineup, self.shop, self.health, self.round)
        c = 0
        while self.gold >= 10 and c<=random.choice([1,2]):
            print(f"do round {self.round} iteration: {c}----------------- \n")
            self.shop = self.get_new_shop_list()
            self.choose_action1(self.lineup, self.shop, self.health, self.round)
            c += 1
        distribute_items()
        sleep(0.5)
        distribute_pieces()
        self.end_round_tasks()

    def shop_to_real_shop(self, shop):
        real_shop = []
        for i, champion_name in shop:
            if champion_name != '':
                real_shop.append((i, game_assets.CHAMPIONS[champion_name]))
        return real_shop

    def get_indices_to_buy(self, lineup, real_shop, round):
        champion_names = []
        for i, champion in real_shop:
            champion_names.append(champion.name)
        counts = Counter(champion_names)
        to_upgrade = []
        for i in counts:
            n = counts[i]
            if n >= 2:
                to_upgrade.append(i)
        indices_to_buy = []
        for i, champion in real_shop:
            if champion.name in to_upgrade or lineup.can_upgrade(champion):
                indices_to_buy.append(i)

        return indices_to_buy

    def buy_champions(self, indices_to_buy, champions_to_buy):
        toggle_shop()
        sleep(0.4)
        for index in indices_to_buy:
            buy_champion(str(index))
        for c in champions_to_buy:
            self.gold -= c.cost
            self.lineup.add_champion(c)
        toggle_shop()
        sleep(0.4)
        distribute_pieces()

    def choose_action1(self, lineup, shop, health, round):
        real_shop = self.shop_to_real_shop(shop)
        print(f'{real_shop =}')
        if round == "1":
            indices_to_buy = [1,2,3,4,5]
        else:
            indices_to_buy = self.get_indices_to_buy(lineup, real_shop, round)
        if len(indices_to_buy) == 0:
            indices_to_buy = [random.choice([1,2,3,4,5])]
        champions_to_buy = []
        for n, c in real_shop:
            if n in indices_to_buy:
                champions_to_buy.append(c)
        print(f'{indices_to_buy=} {champions_to_buy=}')
        self.buy_champions(indices_to_buy, champions_to_buy)

    def choose_action(self, lineup, shop, health, round):
        real_shop = self.shop_to_real_shop(shop)
        count = 0
        for i, champion in real_shop:
            count += 1
            if lineup.can_upgrade(champion):
                index, champion_name = i, champion.name
                break
            else:
                if count == len(real_shop):
                    index, champion_name = max(real_shop, key=lambda c: c[1].value)
                    champion_name = champion_name.name
                    cost = game_assets.CHAMPIONS[champion_name].cost
                    toggle_shop()
                    sleep(0.4)
                    buy_champion(str(index))
                    toggle_shop()
                    sleep(0.4)
                    self.lineup.add_champion(game_assets.CHAMPIONS[champion_name])
                    if int(round) >= 4 and self.gold >= (5 - cost):
                        second_shop = self.get_new_shop_list()
                        print(second_shop)
                        second_shop = self.shop_to_real_shop(second_shop)
                        for j, second_champion in second_shop:
                            if lineup.can_upgrade(second_champion):
                                index, champion_name = j, second_champion.name
                            else:
                                index, champion_name = max(second_shop, key=lambda c: c[1].value)
                                champion_name = champion_name.name
        toggle_shop()
        sleep(0.4)
        buy_champion(str(index))
        toggle_shop()
        sleep(0.4)
        self.lineup.add_champion(game_assets.CHAMPIONS[champion_name])

    def end_round_tasks(self) -> None:
        print(f'{self.lineup=}  {self.health=}')

