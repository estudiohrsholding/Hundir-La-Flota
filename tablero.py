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
        # Es importante cargar las imágenes DESPUÉS de inicializar pygame en la clase Juego
        self.imagenes = {}

    def cargar_imagenes(self):
        """
        Carga, escala y rota todas las imágenes necesarias para el juego.
        Este método DEBE llamarse después de pygame.init().
        """
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
            # Comprobación de límites (aunque ya se hizo antes, es una doble seguridad)
            if not (0 <= cx < self.tamano and 0 <= cy < self.tamano):
                return False
            # Comprobación de superposición y adyacencia
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = cx + j, cy + i
                    if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                        if self.grid[ny][nx] is not None:
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
                    else: # 'v'
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
            # Después del impacto, comprobamos si está hundido
            if barco.esta_hundido():
                # Marcar todas las partes del barco como hundidas
                for pos_x, pos_y in barco.posicion:
                    # Esto es más un cambio de estado lógico que visual
                    pass
                return ESTADO_HUNDIDO
            return ESTADO_IMPACTO
        elif celda is None: # AGUA
            self.grid[y][x] = MARCADOR_FALLO
            return ESTADO_FALLO
        else: # Ya era MARCADOR_FALLO o algo más
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
                    # Determinar si mostrar el barco o agua (si está oculto)
                    if ocultar_barcos and (x, y) not in barco.impactos:
                        surface.blit(self.imagenes['agua'], (rect_x, rect_y))
                    else:
                        # --- Lógica de Sprite Slicing ---
                        try:
                            orient = barco.orientacion.lower()
                            sprite_sheet = self.imagenes[f"{barco.nombre}_{orient}"]
                            slice_index = barco.posicion.index((x,y))

                            if orient == 'h':
                                slice_rect = pygame.Rect(slice_index * TAMANO_CELDA, 0, TAMANO_CELDA, TAMANO_CELDA)
                            else: # 'v'
                                # En vertical, el ancho es el mismo, pero el origen Y cambia
                                slice_rect = pygame.Rect(0, slice_index * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)

                            surface.blit(sprite_sheet, (rect_x, rect_y), slice_rect)

                        except (KeyError, ValueError) as e:
                            # Error: no se encontró el sprite o la posición. Dibujar agua como fallback.
                            surface.blit(self.imagenes['agua'], (rect_x, rect_y))
                            print(f"Error al dibujar barco: {e}")

                    # Dibujar impacto encima si la celda ha sido impactada
                    if (x, y) in barco.impactos:
                        surface.blit(self.imagenes['impacto'], (rect_x, rect_y))

    def todos_hundidos(self):
        return all(barco.esta_hundido() for barco in self.barcos)
