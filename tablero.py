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

        # Cargar, escalar y rotar imágenes de barcos respetando la relación de aspecto
        for nombre, eslora in LISTA_BARCOS:
            img_original = pygame.image.load(ASSETS[nombre]).convert_alpha()
            original_width, original_height = img_original.get_size()

            # Calculate target size for each segment to fit within TAMANO_CELDA x TAMANO_CELDA
            # while maintaining aspect ratio.
            segment_original_width = original_width / eslora if eslora > 0 else original_width
            segment_original_height = original_height

            if segment_original_width == 0 or segment_original_height == 0:
                # Handle cases where image has zero dimension to avoid division by zero or invalid scaling
                new_segment_width = TAMANO_CELDA
                new_segment_height = TAMANO_CELDA
            else:
                scale_factor_width = TAMANO_CELDA / segment_original_width
                scale_factor_height = TAMANO_CELDA / segment_original_height
                scale_factor = min(scale_factor_width, scale_factor_height)

                new_segment_width = int(segment_original_width * scale_factor)
                new_segment_height = int(segment_original_height * scale_factor)

            # Ensure dimensions are at least 1 pixel to avoid issues with pygame.transform.scale
            new_segment_width = max(1, new_segment_width)
            new_segment_height = max(1, new_segment_height)

            # Scale the entire ship image based on the calculated segment size
            final_img_width = new_segment_width * eslora
            final_img_height = new_segment_height

            img_h = pygame.transform.scale(img_original, (final_img_width, final_img_height))
            self.imagenes[f'{nombre}_h'] = img_h
            self.imagenes[f'{nombre}_v'] = pygame.transform.rotate(img_h, 90)

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
                        # --- Sprite Slicing Logic ---
                        slice_index = celda.posicion.index((x,y)) # Índice de la parte del barco en la sprite sheet

                        # Obtener las dimensiones del segmento tal como se escaló en _cargar_imagenes
                        if orient == 'h':
                            segment_width = sprite_sheet.get_width() / celda.eslora
                            segment_height = sprite_sheet.get_height()
                            slice_rect = pygame.Rect(slice_index * segment_width, 0, segment_width, segment_height)
                        else: # 'v'
                            segment_width = sprite_sheet.get_width()
                            segment_height = sprite_sheet.get_height() / celda.eslora
                            slice_rect = pygame.Rect(0, slice_index * segment_height, segment_width, segment_height)

                        # Ahora, centrar la pieza dentro de la celda de TAMANO_CELDA x TAMANO_CELDA
                        target_rect = pygame.Rect(rect_x, rect_y, TAMANO_CELDA, TAMANO_CELDA)

                        # Crear un rect para la imagen rebanada y centrarlo en la celda
                        image_segment_rect = pygame.Rect(0, 0, segment_width, segment_height)
                        image_segment_rect.center = target_rect.center

                        surface.blit(sprite_sheet, image_segment_rect, slice_rect)

                        if (x, y) in barco.impactos:
                            surface.blit(self.imagenes['impacto'], (rect_x, rect_y))

    def todos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)
