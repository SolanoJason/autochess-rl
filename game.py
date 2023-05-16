"""
Handles tasks that happen each game round
"""

from time import sleep, perf_counter
import random
import multiprocessing
import win32gui
import settings
import game_assets
import game_functions
from arena import Arena
from vec4 import Vec4
from vec2 import Vec2


class Game:
    """Clase de juego que maneja la lógica del juego, como tareas redondas."""

    def __init__(self, message_queue: multiprocessing.Queue) -> None:
        self.message_queue = message_queue
        self.arena = Arena(self.message_queue)
        self.round = "0-0"
        self.time: None = None
        self.loading_screen()

    def loading_screen(self) -> None:
        """Bucle que se ejecuta mientras el juego está en la pantalla de carga"""
        game_functions.default_pos()
        while game_functions.get_round() != "1-1":
            sleep(1)
        self.start_time: float = perf_counter()
        self.game_loop()

    def game_loop(self) -> None:
        """. 
        Bucle que se ejecuta mientras el juego está activo, 
        maneja la llamada a las tareas correctas para la ronda y la salida del juego."""
        ran_round: str = None
        while game_functions.check_alive():
            self.round: str = game_functions.get_round()

            if (
                settings.FORFEIT
                and perf_counter() - self.start_time > self.forfeit_time
            ):
                game_functions.forfeit()
                return

            if self.round != ran_round:
                if self.round in game_assets.SECOND_ROUND:
                    self.second_round()
                    ran_round: str = self.round
                elif self.round in game_assets.CAROUSEL_ROUND:
                    self.carousel_round()
                    ran_round: str = self.round
                elif self.round in game_assets.PVE_ROUND:
                    game_functions.default_pos()
                    self.pve_round()
                    ran_round: str = self.round
                elif self.round in game_assets.PVP_ROUND:
                    game_functions.default_pos()
                    self.pvp_round()
                    ran_round: str = self.round
            sleep(0.5)
        self.message_queue.put("CLEAR")
        game_functions.exit_game()

    def second_round(self) -> None:
        print(f"\n[Second Round] {self.round}")
        self.message_queue.put("CLEAR")
        self.arena.bench[0] = "?"
        self.arena.move_unknown()
        self.end_round_tasks()

    def carousel_round(self) -> None:
        print(f"\n[Carousel Round] {self.round}")
        self.message_queue.put("CLEAR")
        if self.round == "3-4":
            self.arena.final_comp = True
        self.arena.check_health()
        print("  Getting a champ from the carousel")
        game_functions.get_champ_carousel(self.round)

    def pve_round(self) -> None:
        print(f"\n[PvE Round] {self.round}")
        self.message_queue.put("CLEAR")
        sleep(0.5)
        if self.round in game_assets.AUGMENT_ROUNDS:
            sleep(1)
            self.arena.pick_augment()
            sleep(2.5)
        if self.round == "1-3":
            sleep(1.5)
            self.arena.fix_unknown()
            self.arena.tacticians_crown_check()

        self.arena.fix_bench_state()
        self.arena.spend_gold()
        self.arena.move_champions()
        self.arena.replace_unknown()
        if self.arena.final_comp:
            self.arena.final_comp_check()
        self.arena.bench_cleanup()
        self.end_round_tasks()

    def pvp_round(self) -> None:
        print(f"\n[PvP Round] {self.round}")
        self.message_queue.put("CLEAR")
        sleep(0.5)
        if self.round in game_assets.AUGMENT_ROUNDS:
            sleep(1)
            self.arena.pick_augment()
            sleep(2.5)
        if self.round in ("2-1", "2-5"):
            self.arena.buy_xp_round()
        if self.round in game_assets.PICKUP_ROUNDS:
            print("  Picking up items")
            game_functions.pickup_items()

        self.arena.fix_bench_state()
        self.arena.bench_cleanup()
        if self.round in game_assets.ANVIL_ROUNDS:
            self.arena.clear_anvil()
        self.arena.spend_gold()
        self.arena.move_champions()
        self.arena.replace_unknown()
        if self.arena.final_comp:
            self.arena.final_comp_check()
        self.arena.bench_cleanup()

        if self.round in game_assets.ITEM_PLACEMENT_ROUNDS:
            sleep(1)
            self.arena.place_items()
        self.end_round_tasks()

    def end_round_tasks(self) -> None:
        self.arena.check_health()
        self.arena.get_label()
        game_functions.default_pos()
