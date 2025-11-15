# constants.py

# Board size
TAMANO_TABLERO = 10

# Ship list (sizes)
LISTA_BARCOS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# Board markers (lo que se ve en el tablero)
AGUA = "~"
BARCO = "B"
MARCADOR_IMPACTO = "X"
MARCADOR_FALLO = "O"

# Game statuses (lo que devuelven las funciones)
ESTADO_IMPACTO = "IMPACTO"
ESTADO_FALLO = "FALLO"
ESTADO_HUNDIDO = "HUNDIDO"
ESTADO_REPETIDO = "REPETIDO"

# --- GUI Constants ---

# RGB Colors
COLOR_AGUA = (22, 100, 150)
COLOR_BARCO = (139, 69, 19)
COLOR_IMPACTO = (220, 20, 60)
COLOR_FALLO = (211, 211, 211)
COLOR_FONDO = (0, 0, 0) # Black
COLOR_TEXTO = (255, 255, 255) # White

# Pixel Dimensions
TAMANO_CELDA = 40
MARGEN_CELDA = 5
TAMANO_TABLERO_PX = TAMANO_TABLERO * (TAMANO_CELDA + MARGEN_CELDA)

# Window Dimensions (calculado para dos tableros y márgenes)
ANCHO_VENTANA = (2 * TAMANO_TABLERO_PX) + (3 * TAMANO_CELDA)
ALTO_VENTANA = TAMANO_TABLERO_PX + (2 * TAMANO_CELDA)
