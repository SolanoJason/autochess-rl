"""
Contiene toda la información relacionada con una ranura de tablero individual utilizada por el bot
"""


class Champion:
    """Clase de campeón que contiene información sobre una sola unidad en el tablero o banco"""

    def __init__(self, ename, coordinates, build, slot, size, final_comp) -> None:
        self.name = ename
        self.coords = coordinates
        self.build = build
        # print(self.build)
        self.index = slot
        self.size = size
        self.completed_items = []
        # print(self.completed_items)
        self.current_building = []
        self.final_comp = final_comp
        print(self.final_comp)

    def does_need_items(self):
        """Devuelve si la instancia de campeón necesita elementos"""
        return len(self.completed_items) != 3 or len(self.build) + len(self.current_building) == 0
