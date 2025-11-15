# Códigos ANSI para colores
ROJO = "\033[91m"
AZUL = "\033[94m"
VERDE = "\033[92m"
RESET = "\033[0m"

def crear_tablero():
    """Crea un tablero vacío de 10x10."""
    return [["~" for _ in range(10)] for _ in range(10)]

def mostrar_tablero(tablero, ocultar_barcos=False, color=None):
    """Muestra el tablero en consola (opcionalmente con color ANSI)."""
    RESET = "\033[0m"  # Código para volver al color normal
    
    # Imprime cabecera de columnas
    header = "  0 1 2 3 4 5 6 7 8 9"
    if color:
        print(f"{color}{header}{RESET}")
    else:
        print(header)

    for i, fila in enumerate(tablero):
        linea = f"{i} "
        for celda in fila:
            if ocultar_barcos and celda == "B":
                linea += "~ "
            elif "X" in celda: # Asegurarse de que X y O existentes también se colorean
                linea += f"{ROJO}X{RESET} "
            elif "O" in celda:
                linea += f"{AZUL}O{RESET} "
            else:
                linea += f"{celda} "
        
        if color:
            print(f"{color}{linea}{RESET}")
        else:
            print(linea)

def marcar_disparo(tablero, x, y):
    """
    Marca el resultado de un disparo en el tablero.
    Devuelve:
    - True: Impacto
    - False: Agua
    - None: Ya se había disparado en esa casilla
    """
    # Comprobar si la celda ya tiene un color (ya disparada)
    if "X" in tablero[y][x] or "O" in tablero[y][x]:
        return None  # Ya disparado
    elif tablero[y][x] == "B":
        tablero[y][x] = f"{ROJO}X{RESET}"  # Impacto en rojo
        return True
    elif tablero[y][x] == "~":
        tablero[y][x] = f"{AZUL}O{RESET}"  # Agua en azul
        return False