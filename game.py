"""
Handles tasks that happen each game round
"""

from time import sleep, perf_counter
import random
import multiprocessing
import win32gui
import settings
import game_assets
from vec4 import Vec4
from vec2 import Vec2
from arena_functions import *
from PIL import Image, ImageGrab


class Game:
    """Clase de juego que maneja la lógica del juego, como tareas redondas."""

    def __init__(self) -> None:
        self.round = "0"
        self.time: None = None
        self.loading_screen()

    def loading_screen(self) -> None:
        """Bucle que se ejecuta mientras el juego está en la pantalla de carga"""
        print("loading screen...")
        screenshot = ImageGrab.grab()
        round = get_round(screenshot)
        print(f'{round=}')
        while round != "1":
            print(f'{round=}')
            sleep(1)
        self.game_loop()

    def game_loop(self) -> None:
        """. 
        Bucle que se ejecuta mientras el juego está activo, 
        maneja la llamada a las tareas correctas para la ronda y la salida del juego."""
        print("game loop:")
        ran_round: str = None
        # while game_functions.check_alive():
        while True:
            screenshot = ImageGrab.grab()
            self.round: str = get_round(screenshot)

            if self.round != ran_round:
                ran_round: str = self.round
                self.do_round()
            sleep(0.5)
        self.message_queue.put("CLEAR")
        game_functions.exit_game()

    def do_round(self):
        print("do round")
        if str(int(self.round)-1) in game_assets.PVE_ROUND:
            toggle_items()
            sleep(1)
            choose_item()
            toggle_items()
        print("toggle_shop")
        toggle_shop()
        sleep(1)
        buy_champion("2")
        toggle_shop()
        distribute_items()
        distribute_pieces()
        self.end_round_tasks()

    def end_round_tasks(self) -> None:
        pass
    
    # def second_round(self) -> None:
    #     print(f"\n[Second Round] {self.round}")
    #     self.message_queue.put("CLEAR")
    #     self.arena.bench[0] = "?"
    #     self.arena.move_unknown()
    #     self.end_round_tasks()

    # def carousel_round(self) -> None:
    #     print(f"\n[Carousel Round] {self.round}")
    #     self.message_queue.put("CLEAR")
    #     if self.round == "3-4":
    #         self.arena.final_comp = True
    #     self.arena.check_health()
    #     print("  Getting a champ from the carousel")
    #     game_functions.get_champ_carousel(self.round)

    # def pve_round(self) -> None:
    #     print(f"\n[PvE Round] {self.round}")
    #     self.message_queue.put("CLEAR")
    #     sleep(0.5)
    #     if self.round in game_assets.AUGMENT_ROUNDS:
    #         sleep(1)
    #         self.arena.pick_augment()
    #         sleep(2.5)
    #     if self.round == "1-3":
    #         sleep(1.5)
    #         self.arena.fix_unknown()
    #         self.arena.tacticians_crown_check()

    #     self.arena.fix_bench_state()
    #     self.arena.spend_gold()
    #     self.arena.move_champions()
    #     self.arena.replace_unknown()
    #     if self.arena.final_comp:
    #         self.arena.final_comp_check()
    #     self.arena.bench_cleanup()
    #     self.end_round_tasks()

    # def pvp_round(self) -> None:
    #     print(f"\n[PvP Round] {self.round}")
    #     self.message_queue.put("CLEAR")
    #     sleep(0.5)
    #     if self.round in game_assets.AUGMENT_ROUNDS:
    #         sleep(1)
    #         self.arena.pick_augment()
    #         sleep(2.5)
    #     if self.round in ("2-1", "2-5"):
    #         self.arena.buy_xp_round()
    #     if self.round in game_assets.PICKUP_ROUNDS:
    #         print("  Picking up items")
    #         game_functions.pickup_items()

    #     self.arena.fix_bench_state()
    #     self.arena.bench_cleanup()
    #     if self.round in game_assets.ANVIL_ROUNDS:
    #         self.arena.clear_anvil()
    #     self.arena.spend_gold()
    #     self.arena.move_champions()
    #     self.arena.replace_unknown()
    #     if self.arena.final_comp:
    #         self.arena.final_comp_check()
    #     self.arena.bench_cleanup()

    #     if self.round in game_assets.ITEM_PLACEMENT_ROUNDS:
    #         sleep(1)
    #         self.arena.place_items()
    #     self.end_round_tasks()

