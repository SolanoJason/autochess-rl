"""
Maneja el estado del tablero/banco dentro del juego y
otras variables utilizadas por el bot para tomar decisiones
"""

from time import sleep
import game_assets
import bot_functions
import screen_coords
from champion import Champion
import ocr
import game_functions
import arena_functions
import comps


class Arena:
    """Clase de arena que maneja la lógica del juego, como el estado del tablero y el banco."""

    def __init__(self, message_queue) -> None:
        self.message_queue = message_queue
        self.tablero_size = 0
        self.banco: list[None] = [None, None, None, None, None, None, None, None, None]
        self.board: list = []
        self.board_unknown: list = []
        self.unknown_slots: list = comps.get_unknown_slots()
        self.campeones_para_comprar: list = comps.champions_to_buy()
        self.tablero_names: list = []
        self.items: list = []
        self.final_comp = False
        self.level = 0
        self.augment_roll = True
        self.spam_roll = False

    def fix_bench_state(self) -> None:
        """Itera a través del banco y corrige las ranuras no válidas"""
        bench_occupied: list = arena_functions.bench_occupied_check()
        for index, slot in enumerate(self.banco):
            if slot is None and bench_occupied[index]:
                self.banco[index] = "?"
            if isinstance(slot, str) and not bench_occupied[index]:
                self.banco[index] = None
            if isinstance(slot, Champion) and not bench_occupied[index]:
                self.banco[index] = None

    def bought_champion(self, name: str, slot: int) -> None:
        """Compra un campeón y crea una instancia de campeón"""
        self.banco[slot] = Champion(name=name,
                                    coords=screen_coords.BENCH_LOC[slot].get_coords(
                                    ),
                                    build=comps.COMP[name]["items"].copy(),
                                    slot=slot,
                                    size=game_assets.CHAMPIONS[name]["Board Size"],
                                    final_comp=comps.COMP[name]["final_comp"])
        bot_functions.move_mouse(screen_coords.DEFAULT_LOC.get_coords())
        sleep(0.5)
        self.fix_bench_state()

    def have_champion(self) -> Champion | None:
        """Revisa el banquillo a ver si existe campeón"""
        return next(
            (
                champion
                for champion in self.banco
                if isinstance(champion, Champion)
                and champion.name not in self.tablero_names
            ),
            None,
        )

    def move_known(self, champion: Champion) -> None:
        """Mueve al campeón al tablero"""
        print(f"  Moving {champion.name} to board")
        destination: tuple = screen_coords.BOARD_LOC[comps.COMP[champion.name]["board_position"]].get_coords()
        bot_functions.left_click(champion.coords)
        sleep(0.1)
        bot_functions.left_click(destination)
        champion.coords = destination
        self.board.append(champion)
        self.tablero_names.append(champion.name)
        self.banco[champion.index] = None
        champion.index = comps.COMP[champion.name]["board_position"]
        self.tablero_size += champion.size

    def move_unknown(self) -> None:
        """Mueve al campeón desconocido al tablero."""
        for index, champion in enumerate(self.banco):
            if isinstance(champion, str):
                print(f"  Moving {champion} to board")
                bot_functions.left_click(screen_coords.BENCH_LOC[index].get_coords())
                sleep(0.1)
                bot_functions.left_click(
                    screen_coords.BOARD_LOC[self.unknown_slots[len(self.board_unknown)]].get_coords())
                self.banco[index] = None
                self.board_unknown.append(champion)
                self.tablero_size += 1
                return

    def sell_bench(self) -> None:
        """Sells all of the champions on the bench"""
        for index, _ in enumerate(self.banco):
            bot_functions.press_e(screen_coords.BENCH_LOC[index].get_coords())
            self.banco[index] = None

    def unknown_in_bench(self) -> bool:
        """Vende a todos los campeones en el banquillo"""
        return any(isinstance(slot, str) for slot in self.banco)

    def move_champions(self) -> None:
        """Mueve campeones al tablero."""
        self.level: int = arena_functions.get_level()
        while self.level > self.tablero_size:
            champion: Champion | None = self.have_champion()
            if champion is not None:
                self.move_known(champion)
            elif self.unknown_in_bench():
                self.move_unknown()
            else:
                bought_unknown = False
                shop: list = arena_functions.get_shop()
                for champion in shop:
                    gold: int = arena_functions.get_gold()
                    valid_champ: bool = (
                        champion[1] in game_assets.CHAMPIONS and
                        game_assets.champion_gold_cost(champion[1]) <= gold and
                        game_assets.champion_board_size(champion[1]) == 1 and
                        champion[1] not in self.campeones_para_comprar and
                        champion[1] not in self.board_unknown
                    )

                    if valid_champ:
                        none_slot: int = arena_functions.empty_slot()
                        bot_functions.left_click(screen_coords.BUY_LOC[champion[0]].get_coords())
                        sleep(0.2)
                        self.banco[none_slot] = f"{champion[1]}"
                        self.move_unknown()
                        bought_unknown = True
                        break

                if not bought_unknown:
                    print("Necesito vender todo el banco para realizar un seguimiento del tablero")
                    self.sell_bench()
                    return

    def replace_unknown(self) -> None:
        """Reemplaza a la campeona desconocida"""
        champion: Champion | None = self.have_champion()
        if len(self.board_unknown) > 0 and champion is not None:
            bot_functions.press_e(screen_coords.BOARD_LOC[self.unknown_slots[len(
                self.board_unknown) - 1]].get_coords())
            self.board_unknown.pop()
            self.tablero_size -= 1
            self.move_known(champion)

    def bench_cleanup(self) -> None:
        for index, champion in enumerate(self.banco):
            if champion == "?" or isinstance(champion, str):
                bot_functions.press_e(screen_coords.BENCH_LOC[index].get_coords())
                self.banco[index] = None
            elif isinstance(champion, Champion):
                if champion.name not in self.campeones_para_comprar and champion.name in self.tablero_names:
                    bot_functions.press_e(screen_coords.BENCH_LOC[index].get_coords())
                    self.banco[index] = None

    def clear_anvil(self) -> None:
        for index, champion in enumerate(self.banco):
            if champion is None:
                bot_functions.press_e(screen_coords.BENCH_LOC[index].get_coords())
        sleep(1)
        bot_functions.left_click(screen_coords.BUY_LOC[2].get_coords())

    def place_items(self) -> None:
        self.items = arena_functions.get_items()
        print(f"  Items: {list(filter((None).__ne__, self.items))}")
        for index, _ in enumerate(self.items):
            if self.items[index] is not None:
                self.add_item_to_champs(index)

    def add_item_to_champs(self, item_index: int) -> None:
        for champ in self.board:
            if champ.does_need_items() and self.items[item_index] is not None:
                self.add_item_to_champ(item_index, champ)

    def add_item_to_champ(self, item_index: int, champ: Champion) -> None:
        item = self.items[item_index]
        if item in game_assets.FULL_ITEMS:
            if item in champ.build:
                bot_functions.left_click(
                    screen_coords.ITEM_POS[item_index][0].get_coords())
                bot_functions.left_click(champ.coords)
                print(f"  Placed {item} on {champ.name}")
                champ.completed_items.append(item)
                champ.build.remove(item)
                self.items[self.items.index(item)] = None
        elif len(champ.current_building) == 0:
            item_to_move: None = None
            for build_item in champ.build:
                build_item_components: list = list(
                    game_assets.FULL_ITEMS[build_item])
                if item in build_item_components:
                    item_to_move: None = item
                    build_item_components.remove(item_to_move)
                    champ.current_building.append(
                        (build_item, build_item_components[0]))
                    champ.build.remove(build_item)
            if item_to_move is not None:
                bot_functions.left_click(
                    screen_coords.ITEM_POS[item_index][0].get_coords())
                bot_functions.left_click(champ.coords)
                print(f"  Placed {item} on {champ.name}")
                self.items[self.items.index(item)] = None
        else:
            for builditem in champ.current_building:
                if item == builditem[1]:
                    bot_functions.left_click(
                        screen_coords.ITEM_POS[item_index][0].get_coords())
                    bot_functions.left_click(champ.coords)
                    champ.completed_items.append(builditem[0])
                    champ.current_building.clear()
                    self.items[self.items.index(item)] = None
                    print(f"  Placed {item} on {champ.name}")
                    print(f"  Completed {builditem[0]}")
                    return

    def fix_unknown(self) -> None:
        sleep(0.25)
        bot_functions.press_e(
            screen_coords.BOARD_LOC[self.unknown_slots[0]].get_coords())
        self.board_unknown.pop(0)
        self.tablero_size -= 1

    def remove_champion(self, champion: Champion) -> None:
        for index, slot in enumerate(self.banco):
            if isinstance(slot, Champion) and slot.name == champion.name:
                bot_functions.press_e(slot.coords)
                self.banco[index] = None

        self.campeones_para_comprar = list(filter(f"{champion.name}".__ne__,
                                         self.campeones_para_comprar))  # Remove all instances of champion in champs_to_buy

        bot_functions.press_e(champion.coords)
        self.tablero_names.remove(champion.name)
        self.tablero_size -= champion.size
        self.board.remove(champion)

    def final_comp_check(self) -> None:
        for slot in self.banco:
            if (
                isinstance(slot, Champion)
                and slot.final_comp
                and slot.name not in self.tablero_names
            ):
                for champion in self.board:
                    if not champion.final_comp and champion.size == slot.size:
                        print(f"  Replacing {champion.name} with {slot.name}")
                        self.remove_champion(champion)
                        self.move_known(slot)
                        break

    def spend_gold(self) -> None:
        """Gasta oro cada ronda"""
        first_run = True
        min_gold = 24 if self.spam_roll else 50
        while first_run or arena_functions.get_gold() >= min_gold:
            if not first_run:
                if arena_functions.get_level() != 9:
                    bot_functions.buy_xp()
                    print("  Purchasing XP")
                bot_functions.reroll()
                print("  Rerolling shop")
            shop: list = arena_functions.get_shop()
            print(f"  Shop: {shop}")
            for champion in shop:
                if (champion[1] in self.campeones_para_comprar and
                    arena_functions.get_gold() - game_assets.CHAMPIONS[champion[1]]["Gold"] >= 0
                 ):
                    none_slot: int = arena_functions.empty_slot()
                    if none_slot != -1:
                        bot_functions.left_click(screen_coords.BUY_LOC[champion[0]].get_coords())
                        print(f"    Purchased {champion[1]}")
                        self.bought_champion(champion[1], none_slot)
                        self.campeones_para_comprar.remove(champion[1])
                    else:
                        print(f"  Board is full but want {champion[1]}")
                        bot_functions.left_click(screen_coords.BUY_LOC[champion[0]].get_coords())
                        game_functions.default_pos()
                        sleep(0.5)
                        self.fix_bench_state()
                        none_slot = arena_functions.empty_slot()
                        sleep(0.5)
                        if none_slot != -1:
                            print(f"    Purchased {champion[1]}")
                            self.campeones_para_comprar.remove(champion[1])
            first_run = False

    def buy_xp_round(self) -> None:
        """Compra XP si el oro es igual o superior a 4"""
        if arena_functions.get_gold() >= 4:
            bot_functions.buy_xp()

        if self.augment_roll:
            print("  Rolling for augment")
            bot_functions.left_click(screen_coords.AUGMENT_ROLL.get_coords())
            self.augment_roll = False
            self.pick_augment()

        bot_functions.left_click(screen_coords.AUGMENT_LOC[0].get_coords())

    def check_health(self) -> None:
        health: int = arena_functions.get_health()
        if health > 0:
            print(f"  Health: {health}")
            if not self.spam_roll and health < 30:
                self.spam_roll = True
        else:
            print("  Health check failed")

    def get_label(self) -> None:
        labels: list = [
            (f"{slot.name}", slot.coords)
            for slot in self.banco
            if isinstance(slot, Champion)
        ]
        for slot in self.board:
            if isinstance(slot, Champion):
                labels.append((f"{slot.name}", slot.coords))

        labels.extend(
            (slot, screen_coords.BOARD_LOC[self.unknown_slots[index]].get_coords())
            for index, slot in enumerate(self.board_unknown)
        )
        self.message_queue.put(("LABEL", labels))
