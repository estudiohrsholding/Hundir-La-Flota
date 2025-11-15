from tablero import crear_tablero, mostrar_tablero
from barcos import definir_barcos, colocar_barcos_aleatorio
from jugador import disparo_jugador, disparo_maquina

# Códigos ANSI (Definidos aquí para que 'juego' los conozca)
VERDE = "\033[92m"
RESET = "\033[0m"

def verificar_fin_juego(tablero):
    """Verifica si quedan barcos ('B') en el tablero."""
    for fila in tablero:
        # Si 'B' (barco sin tocar) está en la celda, el juego sigue.
        # Nota: 'X' coloreado (ej. '\033[91mX\033[0m') no contiene 'B'.
        for celda in fila:
            if celda == "B":
                return False # Todavía quedan barcos
    return True # No quedan 'B'

def jugar_partida():
    """Controla el flujo del juego."""
    tablero_jugador = crear_tablero()
    tablero_maquina = crear_tablero()
    
    barcos_jugador = definir_barcos()
    barcos_maquina = definir_barcos()
    
    colocar_barcos_aleatorio(tablero_jugador, barcos_jugador)
    colocar_barcos_aleatorio(tablero_maquina, barcos_maquina)

    turno = "jugador"
    while True:
        print("\n" + "="*20)
        print("TU TABLERO (Tus barcos 'B', tus fallos 'O', impactos recibidos 'X')")
        
        # --- FIX: Aplicado el argumento de color de Lulule ---
        mostrar_tablero(tablero_jugador, color=VERDE)
        
        print("\nTABLERO ENEMIGO (Tus impactos 'X', tus fallos 'O')")
        mostrar_tablero(tablero_maquina, ocultar_barcos=True)
        print("="*20)

        if turno == "jugador":
            print("\n--- TU TURNO ---")
            acierto = disparo_jugador(tablero_maquina)
            if verificar_fin_juego(tablero_maquina):
                print("\n¡FELICIDADES! ¡HAS GANADO!")
                mostrar_tablero(tablero_maquina) # Muestra el tablero final
                break
            if not acierto: # Si fue agua (False)
                turno = "maquina"
            else:
                print("¡Impacto! Vuelves a disparar.")
        
        else: # Turno de la máquina
            print("\n--- TURNO DE LA MÁQUINA ---")
            acierto = disparo_maquina(tablero_jugador)
            if verificar_fin_juego(tablero_jugador):
                print("\n¡LO SIENTO! ¡LA MÁQUINA HA GANADO!")
                mostrar_tablero(tablero_jugador) # Muestra tu tablero final
                break
            if not acierto: # Si fue agua (False)
                turno = "jugador"
            else:
                print("¡La máquina te ha dado! Vuelve a disparar.")