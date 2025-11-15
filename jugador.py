import random
from tablero import marcar_disparo

# Códigos ANSI para colores
ROJO = "\033[91m"
AZUL = "\033[94m"
RESET = "\033[0m"

def disparo_jugador(tablero_oponente):
    """Pide coordenadas al jugador y dispara."""
    while True:
        try:
            x_str = input(f"Coordenada X (columna) (0-9): ")
            if not x_str: continue
            x = int(x_str)

            y_str = input(f"Coordenada Y (fila) (0-9): ")
            if not y_str: continue
            y = int(y_str)

            if not (0 <= x <= 9 and 0 <= y <= 9):
                print("Coordenadas fuera del tablero. Inténtalo de nuevo.")
                continue

            # Corregido: La entrada del usuario suele ser (X,Y) -> (col, fila)
            # pero el acceso al tablero es (Y,X) -> (fila, col)
            resultado = marcar_disparo(tablero_oponente, x, y)
            
            if resultado is None:
                print("Ya has disparado ahí. Elige otra casilla.")
                continue
            
            if resultado:
                print(f"{ROJO}¡Impacto!{RESET}")
            else:
                print(f"{AZUL}¡Agua!{RESET}")
                
            return resultado # Devuelve True (impacto) o False (agua)

        except ValueError:
            print("Entrada no válida. Introduce números del 0 al 9.")
        except IndexError:
             print("Error inesperado con las coordenadas. Inténtalo de nuevo.")

def disparo_maquina(tablero_jugador):
    """Disparo aleatorio de la máquina."""
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        
        resultado = marcar_disparo(tablero_jugador, x, y)
        
        if resultado is not None: # Si es None, ya había disparado ahí
            print(f"La máquina dispara a ({x}, {y})...")
            if resultado:
                print(f"{ROJO}¡La máquina te ha tocado un barco!{RESET}")
            else:
                print(f"{AZUL}¡La máquina ha fallado y le ha dado al agua!{RESET}")
            return resultado