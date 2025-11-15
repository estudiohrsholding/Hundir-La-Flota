# main.py

from tablero import Tablero
from jugador import JugadorHumano, JugadorMaquina
from constants import (LISTA_BARCOS, VERDE, ROJO, AZUL, RESET,
                       ESTADO_IMPACTO, ESTADO_HUNDIDO, ESTADO_FALLO, ESTADO_REPETIDO)

class Juego:
    """
    Clase principal que orquesta la partida de Batalla Naval.
    """
    def __init__(self):
        """
        Inicializa el juego, creando los tableros y los jugadores.
        """
        self.tablero_jugador = Tablero()
        self.tablero_maquina = Tablero()

        self.tablero_jugador.colocar_barcos_aleatorio(LISTA_BARCOS)
        self.tablero_maquina.colocar_barcos_aleatorio(LISTA_BARCOS)

        self.jugador_humano = JugadorHumano("Jugador", self.tablero_jugador, self.tablero_maquina)
        self.jugador_maquina = JugadorMaquina("Máquina", self.tablero_maquina, self.tablero_jugador)

    def _mostrar_estado(self):
        """
        Muestra los tableros del jugador y de la máquina.
        """
        print("\\n" + "="*30)
        print("TU TABLERO (Tus barcos, tus fallos, impactos recibidos)")
        self.tablero_jugador.mostrar(color=VERDE)

        print("\\nTABLERO ENEMIGO (Tus impactos y fallos)")
        self.tablero_maquina.mostrar(ocultar_barcos=True, color=AZUL)
        print("="*30)

    def run(self):
        """
        Contiene el bucle principal del juego.
        """
        turno_jugador = True

        while True:
            self._mostrar_estado()

            if turno_jugador:
                print(f"\\n{VERDE}--- TU TURNO ---{RESET}")
                resultado = self.jugador_humano.disparar()

                if resultado == ESTADO_IMPACTO:
                    print(f"{ROJO}¡Impacto!{RESET} Sigues tú.")
                elif resultado == ESTADO_HUNDIDO:
                    print(f"{ROJO}¡Hundido!{RESET} ¡Excelente! Sigues tú.")
                elif resultado == ESTADO_FALLO:
                    print(f"{AZUL}¡Agua!{RESET} Turno de la máquina.")
                    turno_jugador = False
                elif resultado == ESTADO_REPETIDO:
                    print("Ya habías disparado ahí. Inténtalo de nuevo.")

                if self.tablero_maquina.todos_hundidos():
                    print("\\n¡FELICIDADES! ¡HAS GANADO LA PARTIDA!")
                    self.tablero_maquina.mostrar(color=VERDE)
                    break

            else: # Turno de la máquina
                print(f"\\n{ROJO}--- TURNO DE LA MÁQUINA ---{RESET}")
                resultado = self.jugador_maquina.disparar()

                if resultado == ESTADO_IMPACTO:
                    print(f"{ROJO}¡La máquina ha impactado uno de tus barcos!{RESET} Sigue la máquina.")
                elif resultado == ESTADO_HUNDIDO:
                    print(f"{ROJO}¡La máquina ha hundido uno de tus barcos!{RESET} Sigue la máquina.")
                elif resultado == ESTADO_FALLO:
                    print(f"{AZUL}¡La máquina ha disparado al agua!{RESET} Tu turno.")
                    turno_jugador = True

                if self.tablero_jugador.todos_hundidos():
                    print("\\n¡LO SIENTO! LA MÁQUINA HA GANADO.")
                    self.tablero_jugador.mostrar(color=ROJO)
                    break

if __name__ == "__main__":
    print("¡Bienvenido a Batalla Naval!")
    juego = Juego()
    juego.run()
