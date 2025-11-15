# jugador.py

import random
from abc import ABC
from constants import TAMANO_TABLERO

class Jugador(ABC):
    """
    Clase base para representar a un jugador.
    """
    def __init__(self, nombre, mi_tablero, tablero_oponente):
        """
        Inicializa un jugador con su nombre y los tableros.
        """
        self.nombre = nombre
        self.mi_tablero = mi_tablero
        self.tablero_oponente = tablero_oponente

class JugadorHumano(Jugador):
    """
    Representa a un jugador humano. La lógica de disparo ahora es
    manejada por eventos en el bucle principal del juego.
    """
    def __init__(self, nombre, mi_tablero, tablero_oponente):
        super().__init__(nombre, mi_tablero, tablero_oponente)


class JugadorMaquina(Jugador):
    """
    Representa a un jugador máquina (IA) que dispara aleatoriamente
    y de forma silenciosa.
    """
    def __init__(self, nombre, mi_tablero, tablero_oponente):
        """
        Inicializa la máquina y un conjunto para recordar los disparos realizados.
        """
        super().__init__(nombre, mi_tablero, tablero_oponente)
        self.disparos_previos = set()

    def disparar(self):
        """
        Genera coordenadas aleatorias hasta encontrar una casilla no disparada.
        Este método ahora es silencioso (no imprime nada).
        """
        while True:
            x = random.randint(0, TAMANO_TABLERO - 1)
            y = random.randint(0, TAMANO_TABLERO - 1)

            if (x, y) not in self.disparos_previos:
                self.disparos_previos.add((x, y))
                # El resultado del disparo se devuelve para que el bucle principal
                # pueda gestionar el estado del juego.
                return self.tablero_oponente.recibir_disparo(x, y)
