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

        self.tablero_jugador = Tablero()
        self.tablero_maquina = Tablero()

        self.tablero_jugador.colocar_barcos_aleatorio(LISTA_BARCOS)
        self.tablero_maquina.colocar_barcos_aleatorio(LISTA_BARCOS)

        self.jugador_humano = JugadorHumano("Jugador", self.tablero_jugador, self.tablero_maquina)
        self.jugador_maquina = JugadorMaquina("Máquina", self.tablero_maquina, self.tablero_jugador)

        self.turno = "humano"
        self.game_over = False
        self.mensaje = ""

    def _pixel_a_grid(self, pixel_x, pixel_y, offset_x, offset_y):
        """
        Convierte coordenadas de píxeles a coordenadas de la cuadrícula del tablero.
        """
        if offset_x <= pixel_x < offset_x + TAMANO_TABLERO_PX and \
           offset_y <= pixel_y < offset_y + TAMANO_TABLERO_PX:

            grid_x = (pixel_x - offset_x) // (TAMANO_CELDA + MARGEN_CELDA)
            grid_y = (pixel_y - offset_y) // (TAMANO_CELDA + MARGEN_CELDA)
            return int(grid_x), int(grid_y)
        return None, None

    def run(self):
        """
        Contiene el bucle principal del juego, manejando eventos, actualizaciones y renderizado.
        """
        offset_jugador_x = TAMANO_CELDA
        offset_tableros_y = TAMANO_CELDA
        offset_maquina_x = offset_jugador_x + TAMANO_TABLERO_PX + TAMANO_CELDA

        while not self.game_over:
            # --- Manejo de Eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.turno == "humano" and event.type == pygame.MOUSEBUTTONDOWN:
                    pixel_x, pixel_y = pygame.mouse.get_pos()
                    grid_x, grid_y = self._pixel_a_grid(pixel_x, pixel_y, offset_maquina_x, offset_tableros_y)

                    if grid_x is not None:
                        resultado = self.tablero_maquina.recibir_disparo(grid_x, grid_y)
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
                else: # Impacto o Hundido
                    self.mensaje = "La máquina ha acertado. Sigue la máquina."

                if self.tablero_jugador.todos_hundidos():
                    self.mensaje = "¡LO SIENTO! LA MÁQUINA HA GANADO."
                    self.game_over = True


            # --- Dibujado ---
            self.screen.fill(COLOR_FONDO)

            # Dibujar tableros
            self.tablero_jugador.mostrar(self.screen, offset_x=offset_jugador_x, offset_y=offset_tableros_y)
            self.tablero_maquina.mostrar(self.screen, offset_x=offset_maquina_x, offset_y=offset_tableros_y, ocultar_barcos=True)

            # Dibujar mensajes
            texto = self.font.render(self.mensaje, True, COLOR_TEXTO)
            self.screen.blit(texto, (20, ALTO_VENTANA - 40))

            pygame.display.flip()
            self.clock.tick(30) # 30 FPS

        # Bucle final para mostrar el resultado
        while True:
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    juego = Juego()
    juego.run()
