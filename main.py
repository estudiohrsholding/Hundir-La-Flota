# main.py

import pygame
import sys
from tablero import Tablero
from jugador import JugadorHumano, JugadorMaquina
from constants import *

class Juego:
    """
    Clase principal que orquesta la partida de Batalla Naval con una GUI de Pygame.
    """
    def __init__(self):
        """
        Inicializa Pygame, la ventana del juego, los tableros y los jugadores.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Batalla Naval")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.offset_jugador = (TAMANO_CELDA, TAMANO_CELDA)
        self.offset_maquina = (TAMANO_TABLERO_PX + 2 * TAMANO_CELDA, TAMANO_CELDA)

        self.tablero_jugador = Tablero()
        self.tablero_maquina = Tablero()

        # Cargar imágenes después de inicializar Pygame
        self.tablero_jugador.cargar_imagenes()
        self.tablero_maquina.cargar_imagenes()

        self.tablero_jugador.colocar_barcos_aleatorio()
        self.tablero_maquina.colocar_barcos_aleatorio()

        self.jugador_humano = JugadorHumano("Jugador", self.tablero_jugador, self.tablero_maquina)
        self.jugador_maquina = JugadorMaquina("Máquina", self.tablero_maquina, self.tablero_jugador)

        self.turno = "humano"
        self.game_over = False
        self.mensaje = "¡Tu turno! Haz clic en el tablero derecho para disparar."

    def _pixel_a_grid(self, pixel_x, pixel_y, offset_x, offset_y):
        """
        Convierte coordenadas de píxeles a coordenadas de la cuadrícula del tablero.
        Devuelve (None, None) si el clic está fuera del tablero.
        """
        # Comprobar si el clic está dentro del área del tablero (sin incluir los márgenes de celda finales)
        board_area_width = self.tablero_maquina.tamano * (TAMANO_CELDA + MARGEN_CELDA) - MARGEN_CELDA
        board_area_height = self.tablero_maquina.tamano * (TAMANO_CELDA + MARGEN_CELDA) - MARGEN_CELDA

        if offset_x <= pixel_x < offset_x + board_area_width and \
           offset_y <= pixel_y < offset_y + board_area_height:

            # Calcular la celda basándose en el tamaño total de celda + margen
            grid_x = (pixel_x - offset_x) // (TAMANO_CELDA + MARGEN_CELDA)
            grid_y = (pixel_y - offset_y) // (TAMANO_CELDA + MARGEN_CELDA)
            return int(grid_x), int(grid_y)
        return None, None

    def run(self):
        """
        Contiene el bucle principal del juego, manejando eventos, actualizaciones y renderizado.
        """
        running = True
        while running:
            # --- Manejo de Eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not self.game_over and self.turno == "humano" and event.type == pygame.MOUSEBUTTONDOWN:
                    pixel_x, pixel_y = pygame.mouse.get_pos()
                    grid_x, grid_y = self._pixel_a_grid(pixel_x, pixel_y, self.offset_maquina[0], self.offset_maquina[1])

                    if grid_x is not None:
                        resultado = self.tablero_maquina.recibir_disparo(grid_x, grid_y)

                        if resultado != ESTADO_REPETIDO:
                            if resultado == ESTADO_FALLO:
                                self.mensaje = "¡Agua! Turno de la máquina."
                                self.turno = "maquina"
                            elif resultado == ESTADO_IMPACTO:
                                self.mensaje = "¡Impacto! Dispara de nuevo."
                            elif resultado == ESTADO_HUNDIDO:
                                self.mensaje = "¡Hundido! Dispara de nuevo."

                            if self.tablero_maquina.todos_hundidos():
                                self.mensaje = "¡FELICIDADES! ¡HAS GANADO!"
                                self.game_over = True

            # --- Turno de la Máquina ---
            if not self.game_over and self.turno == "maquina":
                pygame.time.wait(500) # Pausa para simular pensamiento
                resultado_ia = self.jugador_maquina.disparar()

                if resultado_ia == ESTADO_FALLO:
                    self.mensaje = "La máquina falló. Tu turno."
                    self.turno = "humano"
                elif resultado_ia != ESTADO_REPETIDO: # Impacto o Hundido
                    self.mensaje = "La máquina ha acertado. Sigue la máquina."

                if self.tablero_jugador.todos_hundidos():
                    self.mensaje = "¡LO SIENTO! LA MÁQUINA HA GANADO."
                    self.game_over = True
                # Si es REPETIDO, el turno no cambia y la máquina vuelve a disparar

            # --- Dibujado ---
            self.screen.fill(COLOR_FONDO)
            self.tablero_jugador.mostrar(self.screen, self.offset_jugador[0], self.offset_jugador[1])
            self.tablero_maquina.mostrar(self.screen, self.offset_maquina[0], self.offset_maquina[1], ocultar_barcos=True)
            texto = self.font.render(self.mensaje, True, COLOR_TEXTO)
            self.screen.blit(texto, (20, ALTO_VENTANA - 40))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = Juego()
    juego.run()
