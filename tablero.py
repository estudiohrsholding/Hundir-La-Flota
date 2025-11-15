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
        for eslora, nombre in LISTA_BARCOS:
            img_h = pygame.image.load(ASSETS[nombre]).convert_alpha()

            # Escalar la imagen horizontal para que coincida con la eslora
            scaled_width = TAMANO_CELDA * eslora
            scaled_height = TAMANO_CELDA
            scaled_img_h = pygame.transform.scale(img_h, (scaled_width, scaled_height))

            # Rotar la imagen escalada para la versión vertical
            scaled_img_v = pygame.transform.rotate(scaled_img_h, 90)

            self.imagenes[f'{nombre}_H'] = scaled_img_h
            self.imagenes[f'{nombre}_V'] = scaled_img_v


    def _puede_colocar(self, eslora, x, y, orientacion):
        coords = []
        if orientacion == "H":
            if x + eslora > self.tamano: return False
            coords = [(x + i, y) for i in range(eslora)]
        else: # 'V'
            if y + eslora > self.tamano: return False
            coords = [(x, y + i) for i in range(eslora)]

        for cx, cy in coords:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = cx + j, cy + i
                    if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                        if self.grid[ny][nx] != AGUA:
                            return False
        return True

    def _colocar_barco(self, barco):
        for bx, by in barco.coordenadas:
            self.grid[by][bx] = barco
        self.barcos.append(barco)

    def colocar_barcos_aleatorio(self):
        """
        Crea y coloca barcos aleatoriamente usando la nueva lista de tuplas.
        """
        for eslora, nombre in LISTA_BARCOS:
            colocado = False
            while not colocado:
                x = random.randint(0, self.tamano - 1)
                y = random.randint(0, self.tamano - 1)
                orientacion = random.choice(["H", "V"])
                if self._puede_colocar(eslora, x, y, orientacion):
                    barco = Barco(nombre, eslora, x, y, orientacion)
                    self._colocar_barco(barco)
                    colocado = True

    def recibir_disparo(self, x, y):
        celda = self.grid[y][x]
        if isinstance(celda, Barco):
            barco = celda
            if (x, y) in barco.impactos:
                return ESTADO_REPETIDO

            barco.recibir_impacto(x, y)
            # NO REEMPLAZAR el objeto Barco. La grid debe seguir siendo 'inteligente'.
            # El estado del impacto se gestiona dentro del objeto Barco y se usa
            # en el método `mostrar`.

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

                if isinstance(celda, Barco):
                    barco = celda
                    if (x, y) in barco.impactos:
                        surface.blit(self.imagenes['impacto'], (rect_x, rect_y))
                    else:
                        if ocultar_barcos:
                            surface.blit(self.imagenes['agua'], (rect_x, rect_y))
                        else:
                            # --- Lógica de Sprite Slicing ---
                            parte = barco.get_parte_en_coordenada(x, y)
                            # FIX: La orientación debe ser mayúscula ('H' o 'V') para coincidir
                            # con las claves del diccionario de imágenes.
                            sprite_sheet_key = f"{barco.nombre}_{barco.orientacion.upper()}"
                            sprite_sheet = self.imagenes[sprite_sheet_key]

                            slice_index = barco.coordenadas.index((x, y))

                            slice_x = slice_index * TAMANO_CELDA
                            slice_y = 0

                            slice_rect = pygame.Rect(slice_x, slice_y, TAMANO_CELDA, TAMANO_CELDA)
                            surface.blit(sprite_sheet, (rect_x, rect_y), slice_rect)

                elif celda == MARCADOR_FALLO:
                    surface.blit(self.imagenes['fallo'], (rect_x, rect_y))
                else: # AGUA
                    surface.blit(self.imagenes['agua'], (rect_x, rect_y))


    def todos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)
