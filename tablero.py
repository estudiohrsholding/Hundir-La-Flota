# tablero.py

import random
import pygame
from constants import *
from barco import Barco

class Tablero:
    """
    Gestiona el tablero de juego, incluyendo la colocación de barcos,
    la recepción de disparos y ahora, el dibujado del tablero en una superficie de Pygame.
    """
    def __init__(self, tamano=TAMANO_TABLERO):
        self.tamano = tamano
        self.grid = [[AGUA for _ in range(tamano)] for _ in range(tamano)]
        self.barcos = []

    def _puede_colocar(self, eslora, x, y, orientacion):
        if orientacion == "H":
            if x + eslora > self.tamano: return False
            coords = [(x + i, y) for i in range(eslora)]
        else:
            if y + eslora > self.tamano: return False
            coords = [(x, y + i) for i in range(eslora)]

        for cx, cy in coords:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = cx + j, cy + i
                    if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                        if self.grid[ny][nx] == BARCO:
                            return False
        return True

    def _colocar_barco(self, barco, x, y, orientacion):
        if orientacion == "H":
            barco.posicion = [(x + i, y) for i in range(barco.eslora)]
        else:
            barco.posicion = [(x, y + i) for i in range(barco.eslora)]

        for bx, by in barco.posicion:
            self.grid[by][bx] = BARCO
        self.barcos.append(barco)

    def colocar_barcos_aleatorio(self, lista_esloras):
        for eslora in lista_esloras:
            barco = Barco(eslora)
            colocado = False
            while not colocado:
                x = random.randint(0, self.tamano - 1)
                y = random.randint(0, self.tamano - 1)
                orientacion = random.choice(["H", "V"])
                if self._puede_colocar(eslora, x, y, orientacion):
                    self._colocar_barco(barco, x, y, orientacion)
                    colocado = True

    def recibir_disparo(self, x, y):
        celda = self.grid[y][x]
        if celda == MARCADOR_IMPACTO or celda == MARCADOR_FALLO:
            return ESTADO_REPETIDO

        if celda == AGUA:
            self.grid[y][x] = MARCADOR_FALLO
            return ESTADO_FALLO

        if celda == BARCO:
            self.grid[y][x] = MARCADOR_IMPACTO
            for barco in self.barcos:
                if (x, y) in barco.posicion:
                    barco.impactos.add((x, y))
                    if barco.esta_hundido():
                        return ESTADO_HUNDIDO
                    return ESTADO_IMPACTO
        return "ERROR"

    def mostrar(self, surface, offset_x=0, offset_y=0, ocultar_barcos=False):
        """
        Dibuja el estado actual del tablero en una superficie de Pygame.
        """
        for y, fila in enumerate(self.grid):
            for x, celda in enumerate(fila):
                rect_x = offset_x + x * (TAMANO_CELDA + MARGEN_CELDA)
                rect_y = offset_y + y * (TAMANO_CELDA + MARGEN_CELDA)

                color = COLOR_AGUA # Color por defecto

                if celda == AGUA:
                    color = COLOR_AGUA
                elif celda == MARCADOR_FALLO:
                    color = COLOR_FALLO
                elif celda == MARCADOR_IMPACTO:
                    color = COLOR_IMPACTO
                elif celda == BARCO:
                    if ocultar_barcos:
                        color = COLOR_AGUA
                    else:
                        color = COLOR_BARCO

                pygame.draw.rect(surface, color, (rect_x, rect_y, TAMANO_CELDA, TAMANO_CELDA))

    def todos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)
