# constants.py

# ANSI color codes
ROJO = "\\033[91m"
AZUL = "\\033[94m"
VERDE = "\\033[92m"
RESET = "\\033[0m"

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
