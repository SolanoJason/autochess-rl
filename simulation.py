import gym
from gym import spaces
import numpy as np

class TiendaEnv(gym.Env):
    def __init__(self):
        super(TiendaEnv, self).__init__()

        self.total_piezas = 96
        self.tamano_tienda = 5
        self.acciones_disponibles = self.total_piezas // self.tamano_tienda

        self.tienda = None
        self.estado = None

        self.action_space = spaces.Discrete(self.acciones_disponibles)
        self.observation_space = spaces.Discrete(self.total_piezas)

    def reset(self):
        self.tienda = np.random.choice(self.total_piezas, size=self.tamano_tienda, replace=False)
        self.estado = self.tienda.copy()
        return self.estado

    def step(self, accion):
        assert self.action_space.contains(accion), "Accion no valida"

        recompensa = 0

        if accion != 0:
            self.tienda = np.random.choice(self.total_piezas, size=self.tamano_tienda, replace=False)
            self.estado = self.tienda.copy()
            recompensa = 1

        observacion = self.estado.copy()
        done = False

        return observacion, recompensa, done, {}

    def render(self):
        print("Tienda:", self.tienda)

# Crear una instancia del entorno
env = TiendaEnv()

# Reiniciar el entorno
estado_inicial = env.reset()
print("Estado inicial:", estado_inicial)

# Realizar algunos pasos en el juego
accion = 1
observacion, recompensa, done, _ = env.step(accion)
print("Observacion:", observacion)
print("Recompensa:", recompensa)
print("Done:", done)

# Renderizar la tienda actual
env.render()
