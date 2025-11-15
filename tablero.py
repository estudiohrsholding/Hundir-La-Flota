# tablero.py

import random
import pygame
from constants import *
from barco import Barco

class Tablero:
    """
    Gestiona el tablero de juego, incluyendo la colocación de barcos,
    la recepción de disparos y, ahora, el dibujado del tablero con sprites.
    """
    def __init__(self, tamano=TAMANO_TABLERO):
        self.tamano = tamano
        self.grid = [[AGUA for _ in range(tamano)] for _ in range(tamano)]
        self.barcos = []
        self._cargar_imagenes()

    def _cargar_imagenes(self):
        """
        Carga, escala y rota todas las imágenes necesarias para el juego.
        Este método es privado y se llama solo una vez desde __init__.
        """
        self.imagenes = {}

        # Cargar imágenes de celdas básicas
        for asset_name in ['agua', 'fallo', 'impacto']:
            img = pygame.image.load(ASSETS[asset_name]).convert_alpha()
            self.imagenes[asset_name] = pygame.transform.scale(img, (TAMANO_CELDA, TAMANO_CELDA))

        # Cargar, escalar y rotar imágenes de barcos
        for nombre, eslora in LISTA_BARCOS:
            img_h = pygame.image.load(ASSETS[nombre]).convert_alpha()
            self.imagenes[f'{nombre}_h'] = pygame.transform.scale(img_h, (TAMANO_CELDA * eslora, TAMANO_CELDA))
            self.imagenes[f'{nombre}_v'] = pygame.transform.rotate(self.imagenes[f'{nombre}_h'], 90)

    def _puede_colocar(self, barco, x, y, orientacion):
        coords = []
        if orientacion == "h":
            if x + barco.eslora > self.tamano: return False
            coords = [(x + i, y) for i in range(barco.eslora)]
        else: # 'v'
            if y + barco.eslora > self.tamano: return False
            coords = [(x, y + i) for i in range(barco.eslora)]

        for cx, cy in coords:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = cx + j, cy + i
                    if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                        if self.grid[ny][nx] != AGUA:
                            return False
        return True


    def colocar_barcos_aleatorio(self):
        """
        Crea y coloca barcos aleatoriamente usando la nueva lista de tuplas.
        """
        for nombre, eslora in LISTA_BARCOS:
            barco = Barco(eslora, nombre)
            colocado = False
            while not colocado:
                x = random.randint(0, self.tamano - 1)
                y = random.randint(0, self.tamano - 1)
                orientacion = random.choice(["h", "v"])
                if self._puede_colocar(barco, x, y, orientacion):
                    barco.x = x
                    barco.y = y
                    barco.orientacion = orientacion
                    if orientacion == 'h':
                        for i in range(eslora):
                            self.grid[y][x+i] = barco
                            barco.posicion.append((x+i, y))
                    else:
                        for i in range(eslora):
                            self.grid[y+i][x] = barco
                            barco.posicion.append((x, y+i))
                    self.barcos.append(barco)
                    colocado = True


    def recibir_disparo(self, x, y):
        celda = self.grid[y][x]
        if isinstance(celda, Barco):
            barco = celda
            if (x, y) in barco.impactos:
                return ESTADO_REPETIDO

            barco.recibir_impacto(x, y)
            if barco.esta_hundido():
                return ESTADO_HUNDIDO
            return ESTADO_IMPACTO
        elif celda == AGUA:
            self.grid[y][x] = MARCADOR_FALLO
            return ESTADO_FALLO
        else: # Ya era MARCADOR_FALLO
            return ESTADO_REPETIDO

    def mostrar(self, surface, offset_x=0, offset_y=0, ocultar_barcos=False):
        """
        Dibuja el estado actual del tablero usando la técnica de "Sprite Slicing".
        """
        for y, fila in enumerate(self.grid):
            for x, celda in enumerate(fila):
                rect_x = offset_x + x * (TAMANO_CELDA + MARGEN_CELDA)
                rect_y = offset_y + y * (TAMANO_CELDA + MARGEN_CELDA)

                if celda is None:
                    surface.blit(self.imagenes['agua'], (rect_x, rect_y))
                elif celda == MARCADOR_FALLO:
                    surface.blit(self.imagenes['fallo'], (rect_x, rect_y))
                elif isinstance(celda, Barco):
                    barco = celda
                    if ocultar_barcos:
                        if (x, y) in barco.impactos:
                            surface.blit(self.imagenes['impacto'], (rect_x, rect_y))
                        else:
                            surface.blit(self.imagenes['agua'], (rect_x, rect_y))
                    else:
                        # --- Sprite Slicing Logic ---
                        parte = celda.get_parte_en_coord(x, y)
                        orient = celda.orientacion.lower()
                        sprite_sheet = self.imagenes[f"{celda.nombre}_{orient}"]
                        # Calculate which slice (subsurface) to cut based on 'parte' and 'orientacion'
                        slice_index = celda.posicion.index((x,y))
                        if orient == 'h':
                            slice_rect = pygame.Rect(slice_index * TAMANO_CELDA, 0, TAMANO_CELDA, TAMANO_CELDA)
                        else: # 'v'
                            slice_rect = pygame.Rect(0, slice_index * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                        surface.blit(sprite_sheet, (rect_x, rect_y), slice_rect)
                        if (x, y) in barco.impactos:
                            surface.blit(self.imagenes['impacto'], (rect_x, rect_y))

    def todos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)
