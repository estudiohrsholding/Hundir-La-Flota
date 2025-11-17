# main.py
import clases
import funciones
import time

def run_game():
    """
    Función principal que orquesta el juego de Batalla Naval.
    """
    print("="*30)
    print("¡Bienvenido a Batalla Naval!")
    print("="*30)
    print("Reglas: 'B' es un barco, 'X' es un impacto, 'O' es un fallo.")

    # Inicialización de los tableros
    tablero_jugador = clases.Tablero(id_jugador='Player')
    tablero_maquina = clases.Tablero(id_jugador='AI')

    # Colocación de barcos
    print("\nColocando tus barcos...")
    tablero_jugador.inicializar_barcos()
    print("Colocando los barcos de la IA...")
    tablero_maquina.inicializar_barcos()

    turno = 'Player'

    while True:
        print("\n" + "="*30)
        if turno == 'Player':
            print("--- TU TURNO ---")

            # Mostrar tableros
            print("\nTU TABLERO:")
            tablero_jugador.mostrar_tablero(tipo_vista='privado')
            print("\nTABLERO DE LA IA:")
            tablero_maquina.mostrar_tablero(tipo_vista='publico')

            # Pedir coordenadas y disparar
            while True:
                x, y = funciones.pedir_coordenadas()
                resultado = tablero_maquina.recibir_disparo(x, y)

                if resultado is None:
                    print("Ya has disparado en estas coordenadas. Inténtalo de nuevo.")
                else:
                    break

            if resultado:
                print("\n¡IMPACTO! Vuelves a disparar.")
                if tablero_maquina.comprobar_victoria():
                    print("\n¡FELICIDADES, HAS GANADO!")
                    tablero_maquina.mostrar_tablero(tipo_vista='privado')
                    break
            else:
                print("\n¡AGUA! Turno de la IA.")
                turno = 'AI'

        else: # Turno de la IA
            print("--- TURNO DE LA IA ---")
            time.sleep(1) # Pequeña pausa para simular pensamiento

            # Disparo de la máquina (con reintento si la casilla ya fue disparada)
            while True:
                x, y = funciones.disparo_maquina()
                resultado = tablero_jugador.recibir_disparo(x, y)

                if resultado is not None:
                    print(f"La IA dispara a ({x}, {y})...")
                    break

            if resultado:
                print("\n¡IMPACTO! La IA vuelve a disparar.")
                if tablero_jugador.comprobar_victoria():
                    print("\n¡LO SIENTO, LA IA HA GANADO!")
                    tablero_jugador.mostrar_tablero(tipo_vista='privado')
                    break
            else:
                print("\n¡AGUA! Tu turno.")
                turno = 'Player'

if __name__ == '__main__':
    run_game()
