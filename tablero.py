# tablero.py

import random
from constants import (TAMANO_TABLERO, AGUA, BARCO,
                       MARCADOR_IMPACTO, MARCADOR_FALLO,
                       ESTADO_IMPACTO, ESTADO_FALLO, ESTADO_HUNDIDO, ESTADO_REPETIDO,
                       ROJO, AZUL, VERDE, RESET)
from barco import Barco

class Tablero:
    """
    Gestiona el tablero de juego, incluyendo la colocación de barcos,
    la recepción de disparos y la visualización del estado.
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

    def mostrar(self, ocultar_barcos=False, color=None):
        color_final = color if color else ""
        print(f"{color_final}  {' '.join(map(str, range(self.tamano)))}{RESET}")

        for i, fila in enumerate(self.grid):
            linea_mostrada = f"{color_final}{i} "
            for celda in fila:
                if ocultar_barcos and celda == BARCO:
                    linea_mostrada += f"{AGUA} "
                elif celda == MARCADOR_IMPACTO:
                    linea_mostrada += f"{ROJO}{MARCADOR_IMPACTO}{RESET}{color_final} "
                elif celda == MARCADOR_FALLO:
                    linea_mostrada += f"{AZUL}{MARCADOR_FALLO}{RESET}{color_final} "
                elif celda == BARCO:
                     linea_mostrada += f"{VERDE}{BARCO}{RESET}{color_final} "
                else:
                    linea_mostrada += f"{celda} "
            print(f"{linea_mostrada.strip()}{RESET}")

    def todos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)
