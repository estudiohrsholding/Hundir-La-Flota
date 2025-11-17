# funciones.py
import random
import variables as var

def pedir_coordenadas():
    """
    Pide al jugador que introduzca coordenadas para un disparo.
    Valida que las coordenadas estén dentro del tablero y sean numéricas.

    Devuelve:
        - tuple (int, int): Coordenadas (x, y) validadas.
    """
    while True:
        try:
            x_str = input(f"Coordenada X (columna, 0-{var.TAMANO_TABLERO - 1}): ")
            if not x_str: continue
            x = int(x_str)

            y_str = input(f"Coordenada Y (fila, 0-{var.TAMANO_TABLERO - 1}): ")
            if not y_str: continue
            y = int(y_str)

            if not (0 <= x < var.TAMANO_TABLERO and 0 <= y < var.TAMANO_TABLERO):
                print("Coordenadas fuera del tablero. Inténtalo de nuevo.")
                continue

            return x, y

        except ValueError:
            print(f"Entrada no válida. Introduce números enteros entre 0 y {var.TAMANO_TABLERO - 1}.")
        except IndexError:
            print("Error inesperado con las coordenadas. Inténtalo de nuevo.")

def disparo_maquina():
    """
    Genera coordenadas aleatorias para el disparo de la máquina.

    Devuelve:
        - tuple (int, int): Coordenadas (x, y) aleatorias.
    """
    x = random.randint(0, var.TAMANO_TABLERO - 1)
    y = random.randint(0, var.TAMANO_TABLERO - 1)
    return x, y
