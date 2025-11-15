# jugador.py

import random
from abc import ABC, abstractmethod
from constants import TAMANO_TABLERO

class Jugador(ABC):
    """
    Clase base abstracta para representar a un jugador.
    """
    def __init__(self, nombre, mi_tablero, tablero_oponente):
        """
        Inicializa un jugador con su nombre y los tableros.
        """
        self.nombre = nombre
        self.mi_tablero = mi_tablero
        self.tablero_oponente = tablero_oponente

    @abstractmethod
    def disparar(self):
        """
        Método abstracto para que el jugador realice un disparo.
        Debe ser implementado por las subclases.
        """
        pass

class JugadorHumano(Jugador):
    """
    Representa a un jugador humano que introduce coordenadas manualmente.
    """
    def disparar(self):
        """
        Pide al usuario coordenadas, valida la entrada y gestiona el disparo.
        """
        while True:
            try:
                x_str = input(f"[{self.nombre}] Coordenada X (columna, 0-{TAMANO_TABLERO - 1}): ")
                if not x_str: continue
                x = int(x_str)

                y_str = input(f"[{self.nombre}] Coordenada Y (fila, 0-{TAMANO_TABLERO - 1}): ")
                if not y_str: continue
                y = int(y_str)

                if not (0 <= x < TAMANO_TABLERO and 0 <= y < TAMANO_TABLERO):
                    print("Coordenadas fuera del tablero. Inténtalo de nuevo.")
                    continue

                return self.tablero_oponente.recibir_disparo(x, y)

            except ValueError:
                print("Entrada no válida. Introduce números del 0 al 9.")
            except IndexError:
                print("Error inesperado con las coordenadas. Inténtalo de nuevo.")

class JugadorMaquina(Jugador):
    """
    Representa a un jugador máquina (IA) que dispara aleatoriamente.
    """
    def __init__(self, nombre, mi_tablero, tablero_oponente):
        """
        Inicializa la máquina y un conjunto para recordar los disparos realizados.
        """
        super().__init__(nombre, mi_tablero, tablero_oponente)
        self.disparos_realizados = set()

    def disparar(self):
        """
        Genera coordenadas aleatorias hasta encontrar una casilla no disparada.
        """
        while True:
            x = random.randint(0, TAMANO_TABLERO - 1)
            y = random.randint(0, TAMANO_TABLERO - 1)

            if (x, y) not in self.disparos_realizados:
                self.disparos_realizados.add((x, y))
                print(f"La máquina dispara a ({x}, {y})...")
                return self.tablero_oponente.recibir_disparo(x, y)
