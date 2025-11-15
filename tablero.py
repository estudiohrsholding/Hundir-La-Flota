# tablero.py

import random
import pygame
from constants import *
from barco import Barco

class Tablero:
    """
    Gestiona el tablero de juego, incluyendo la colocación de barcos,
    la recepción de disparos y el dibujado del tablero.
    La grid ahora almacena referencias a objetos Barco en lugar de 'B'.
    """
    def __init__(self, tamano=TAMANO_TABLERO):
        self.tamano = tamano
        # La grid ahora contendrá AGUA o referencias a instancias de Barco.
        self.grid = [[AGUA for _ in range(tamano)] for _ in range(tamano)]
        self.barcos = []

    def _puede_colocar(self, eslora, x, y, orientacion):
        """
        Verifica si un barco puede ser colocado en las coordenadas y
        orientación dadas sin solaparse o estar demasiado cerca de otros.
        """
        coords = []
        if orientacion == "H":
            if x + eslora > self.tamano: return False
            coords = [(x + i, y) for i in range(eslora)]
        else: # 'V'
            if y + eslora > self.tamano: return False
            coords = [(x, y + i) for i in range(eslora)]

        for cx, cy in coords:
            # Comprobación de área circundante (buffer de 1 celda)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = cx + j, cy + i
                    if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                        # Si la celda no es AGUA, es que hay otro barco
                        if self.grid[ny][nx] != AGUA:
                            return False
        return True

    def _colocar_barco(self, barco):
        """
        Coloca un barco (ya inicializado con coordenadas) en la grid.
        """
        for bx, by in barco.coordenadas:
            self.grid[by][bx] = barco # Almacena la referencia al objeto
        self.barcos.append(barco)

    def colocar_barcos_aleatorio(self, lista_esloras):
        """
        Crea y coloca barcos de diferentes esloras aleatoriamente en el tablero.
        """
        for eslora in lista_esloras:
            colocado = False
            while not colocado:
                x = random.randint(0, self.tamano - 1)
                y = random.randint(0, self.tamano - 1)
                orientacion = random.choice(["H", "V"])
                if self._puede_colocar(eslora, x, y, orientacion):
                    # Crea el barco con su posición final
                    barco = Barco(eslora, x, y, orientacion)
                    self._colocar_barco(barco)
                    colocado = True

    def recibir_disparo(self, x, y):
        """
        Procesa un disparo en las coordenadas (x, y) y devuelve el
        estado resultante.
        """
        celda = self.grid[y][x]

        # Si la celda es un objeto Barco, es un impacto.
        if isinstance(celda, Barco):
            barco = celda
            # Si ya ha sido impactado en esa misma celda
            if (x, y) in barco.impactos:
                return ESTADO_REPETIDO

            barco.recibir_impacto(x, y)
            if barco.esta_hundido():
                return ESTADO_HUNDIDO
            return ESTADO_IMPACTO

        # Si no es un barco, debe ser AGUA, FALLO o IMPACTO
        elif celda == AGUA:
            self.grid[y][x] = MARCADOR_FALLO
            return ESTADO_FALLO

        # Si disparamos a un fallo anterior
        elif celda == MARCADOR_FALLO:
            return ESTADO_REPETIDO

        # Este caso es teóricamente imposible si el estado se gestiona bien
        # (no debería haber marcadores de impacto en la grid de barcos)
        # pero se incluye por robustez.
        else:
            return ESTADO_REPETIDO


    def mostrar(self, surface, offset_x=0, offset_y=0, ocultar_barcos=False):
        """
        Dibuja el estado actual del tablero en una superficie de Pygame.
        """
        for y, fila in enumerate(self.grid):
            for x, celda in enumerate(fila):
                rect_x = offset_x + x * (TAMANO_CELDA + MARGEN_CELDA)
                rect_y = offset_y + y * (TAMANO_CELDA + MARGEN_CELDA)

                color = COLOR_AGUA # Color por defecto

                if isinstance(celda, Barco):
                    barco = celda
                    if (x, y) in barco.impactos:
                        color = COLOR_IMPACTO
                    else:
                        color = COLOR_AGUA if ocultar_barcos else COLOR_BARCO

                elif celda == AGUA:
                    color = COLOR_AGUA
                elif celda == MARCADOR_FALLO:
                    color = COLOR_FALLO
                # No necesitamos un caso para MARCADOR_IMPACTO porque
                # los impactos se gestionan a través del estado del objeto Barco.

                pygame.draw.rect(surface, color, (rect_x, rect_y, TAMANO_CELDA, TAMANO_CELDA))

    def todos_hundidos(self):
        """
        Verifica si todos los barcos en el tablero han sido hundidos.
        """
        return all(barco.esta_hundido() for barco in self.barcos)
