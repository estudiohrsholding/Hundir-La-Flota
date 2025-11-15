import random

def definir_barcos():
    """Devuelve una lista con los tamaños de los barcos."""
    # 1x4, 2x3, 3x2, 4x1 (Total: 10 barcos, 20 casillas)
    return [4] + [3]*2 + [2]*3 + [1]*4

def colocar_barcos_aleatorio(tablero, lista_barcos):
    """Coloca barcos aleatoriamente en el tablero."""
    for eslora in lista_barcos:
        colocado = False
        while not colocado:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            orientacion = random.choice(["H", "V"])
            if puede_colocar(tablero, x, y, eslora, orientacion):
                colocar(tablero, x, y, eslora, orientacion)
                colocado = True

def puede_colocar(tablero, x, y, eslora, orientacion):
    """Verifica si se puede colocar el barco (sin solaparse)."""
    if orientacion == "H":
        if x + eslora > 10:
            return False
        # Comprueba solo la posición (lógica de colisión simple)
        return all(tablero[y][x+i] == "~" for i in range(eslora))
    else:
        if y + eslora > 10:
            return False
        # Comprueba solo la posición (lógica de colisión simple)
        return all(tablero[y+i][x] == "~" for i in range(eslora))

def colocar(tablero, x, y, eslora, orientacion):
    """Coloca el barco en el tablero."""
    for i in range(eslora):
        if orientacion == "H":
            tablero[y][x+i] = "B"
        else:
            tablero[y+i][x] = "B"